from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from .models import Vehicle, Fine, ViolationType, NotificationLog
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET"])
def vehicle_details(request):
    """Fetch vehicle details by number plate"""
    try:
        number_plate = request.GET.get('number_plate', '').strip().upper()
        
        if not number_plate:
            return JsonResponse({'error': 'Number plate is required'}, status=400)
        
        vehicle = Vehicle.objects.select_related('owner_name').get(
            number_plate=number_plate
        )
        
        return JsonResponse({
            'id': vehicle.id,
            'number_plate': vehicle.number_plate,
            'vehicle_type': vehicle.vehicle_type,
            'vehicle_model': vehicle.vehicle_model,
            'vehicle_number': vehicle.vehicle_number,
            'owner_name': vehicle.owner_name.get_full_name() or vehicle.owner_name.username,
            'owner_phone': vehicle.owner_phone,
            'owner_address': vehicle.owner_address,
            'registration_date': vehicle.registration_date.isoformat() if vehicle.registration_date else None,
        }, status=200)
    
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching vehicle details: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@transaction.atomic
def create_fine(request):
    """Create a new fine with vehicle and violation details"""
    try:
        # Extract form data
        number_plate = request.POST.get('number_plate', '').strip().upper()
        vehicle_type = request.POST.get('vehicle_type', '').strip()
        vehicle_number = request.POST.get('vehicle_number', '').strip()
        vehicle_model = request.POST.get('vehicle_model', '').strip()
        fine_amount = request.POST.get('fine_amount')
        explanation = request.POST.get('explanation', '').strip()
        photo_proof = request.FILES.get('photo_proof')
        
        # Validate required fields
        if not all([number_plate, vehicle_type, fine_amount, explanation, photo_proof]):
            return JsonResponse({
                'error': 'Missing required fields: number_plate, vehicle_type, fine_amount, explanation, photo_proof'
            }, status=400)
        
        # Validate fine amount
        try:
            fine_amount = float(fine_amount)
            if fine_amount < 0:
                return JsonResponse({'error': 'Fine amount must be positive'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid fine amount'}, status=400)
        
        # Validate photo file
        if not photo_proof.content_type.startswith('image/'):
            return JsonResponse({'error': 'Photo proof must be an image file'}, status=400)
        
        # Get or create vehicle
        vehicle, created = Vehicle.objects.get_or_create(
            number_plate=number_plate,
            defaults={
                'vehicle_type': vehicle_type,
                'vehicle_model': vehicle_model,
                'vehicle_number': vehicle_number,
                'owner_phone': 'N/A',
                'owner_name': get_or_create_default_user()
            }
        )
        
        # Update vehicle info if it exists
        if not created:
            if vehicle_model:
                vehicle.vehicle_model = vehicle_model
            if vehicle_number:
                vehicle.vehicle_number = vehicle_number
            vehicle.vehicle_type = vehicle_type
            vehicle.save()
        
        # Get or create violation type based on explanation keywords
        violation_type = get_or_create_violation_type(explanation, fine_amount)
        
        # Create the fine
        fine = Fine.objects.create(
            vehicle=vehicle,
            violation_type=violation_type,
            violation_explanation=explanation,
            violation_date=timezone.now(),
            fine_amount=fine_amount,
            photo_proof=photo_proof,
            status='Issued'
        )
        
        # Create notification log
        NotificationLog.objects.create(
            fine=fine,
            notification_type='App',
            recipient=vehicle.owner_phone,
            message=f"Traffic fine of ₹{fine_amount} issued for {vehicle.number_plate}. "
                   f"Violation: {explanation}. Please acknowledge and pay within 30 days.",
            status='Pending'
        )
        
        return JsonResponse({
            'message': 'Fine created successfully',
            'fine_id': fine.id,
            'vehicle_id': vehicle.id,
            'status': fine.status,
            'fine_amount': str(fine.fine_amount),
            'notification_status': 'pending'
        }, status=201)
    
    except Exception as e:
        logger.error(f"Error creating fine: {str(e)}")
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)


def get_or_create_default_user():
    """Get or create a default user for vehicles without owner info"""
    user, created = User.objects.get_or_create(
        username='vehicle_owner_default',
        defaults={
            'first_name': 'Vehicle',
            'last_name': 'Owner'
        }
    )
    return user


def get_or_create_violation_type(explanation, fine_amount):
    """Get or create violation type based on keywords in explanation"""
    keywords = {
        'red light': ('Jumping Red Light', 'Severe'),
        'parking': ('Improper Parking', 'Minor'),
        'speeding': ('Speeding', 'Severe'),
        'helmet': ('Not Wearing Helmet', 'Minor'),
        'seatbelt': ('Not Wearing Seatbelt', 'Minor'),
        'overtaking': ('Improper Overtaking', 'Moderate'),
        'lane': ('Wrong Lane Usage', 'Moderate'),
        'signal': ('No Signal', 'Moderate'),
    }
    
    violation_name = 'Other Traffic Violation'
    severity = 'Moderate'
    
    explanation_lower = explanation.lower()
    for keyword, (name, sev) in keywords.items():
        if keyword in explanation_lower:
            violation_name = name
            severity = sev
            break
    
    violation_type, created = ViolationType.objects.get_or_create(
        name=violation_name,
        defaults={
            'description': f'Violation: {violation_name}',
            'default_fine_amount': fine_amount,
            'severity': severity
        }
    )
    
    return violation_type


@csrf_exempt
@require_http_methods(["GET"])
def get_fines_by_vehicle(request):
    """Get all fines for a specific vehicle"""
    try:
        number_plate = request.GET.get('number_plate', '').strip().upper()
        
        if not number_plate:
            return JsonResponse({'error': 'Number plate is required'}, status=400)
        
        vehicle = Vehicle.objects.get(number_plate=number_plate)
        fines = vehicle.fines.all().values(
            'id', 'violation_explanation', 'fine_amount', 'status',
            'violation_date', 'issued_at', 'paid_at'
        )
        
        return JsonResponse({
            'vehicle': {
                'number_plate': vehicle.number_plate,
                'owner_name': vehicle.owner_name.get_full_name() or vehicle.owner_name.username,
            },
            'total_fines': vehicle.fines.count(),
            'total_amount': sum(f['fine_amount'] for f in fines),
            'fines': list(fines)
        }, status=200)
    
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching fines: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_fine_details(request, fine_id):
    """Get detailed information about a specific fine"""
    try:
        fine = Fine.objects.select_related(
            'vehicle', 'issued_by', 'violation_type'
        ).get(id=fine_id)
        
        return JsonResponse({
            'id': fine.id,
            'vehicle': {
                'number_plate': fine.vehicle.number_plate,
                'type': fine.vehicle.vehicle_type,
                'owner': fine.vehicle.owner_name.get_full_name() or fine.vehicle.owner_name.username,
                'phone': fine.vehicle.owner_phone,
            },
            'violation': {
                'type': fine.violation_type.name if fine.violation_type else 'Other',
                'explanation': fine.violation_explanation,
                'date': fine.violation_date.isoformat(),
                'location': fine.location,
            },
            'fine_amount': str(fine.fine_amount),
            'status': fine.status,
            'issued_at': fine.issued_at.isoformat(),
            'paid_at': fine.paid_at.isoformat() if fine.paid_at else None,
            'photo_proof': fine.photo_proof.url if fine.photo_proof else None,
        }, status=200)
    
    except Fine.DoesNotExist:
        return JsonResponse({'error': 'Fine not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching fine details: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_fine_status(request, fine_id):
    """Update the status of a fine"""
    try:
        fine = Fine.objects.get(id=fine_id)
        new_status = request.POST.get('status', '').strip()
        
        valid_statuses = ['Issued', 'Notified', 'Acknowledged', 'Paid', 'Disputed', 'Cancelled']
        if new_status not in valid_statuses:
            return JsonResponse({
                'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }, status=400)
        
        fine.status = new_status
        
        if new_status == 'Notified':
            fine.notification_sent_at = timezone.now()
        elif new_status == 'Acknowledged':
            fine.acknowledged_at = timezone.now()
        elif new_status == 'Paid':
            fine.paid_at = timezone.now()
        
        fine.save()
        
        return JsonResponse({
            'message': f'Fine status updated to {new_status}',
            'fine_id': fine.id,
            'status': fine.status,
        }, status=200)
    
    except Fine.DoesNotExist:
        return JsonResponse({'error': 'Fine not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating fine status: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_statistics(request):
    """Get overall fine statistics"""
    try:
        from django.db.models import Count, Sum
        from datetime import timedelta
        
        total_fines = Fine.objects.count()
        total_revenue = Fine.objects.aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
        fines_paid = Fine.objects.filter(status='Paid').count()
        revenue_collected = Fine.objects.filter(status='Paid').aggregate(
            Sum('fine_amount')
        )['fine_amount__sum'] or 0
        
        # Last 7 days stats
        seven_days_ago = timezone.now() - timedelta(days=7)
        fines_this_week = Fine.objects.filter(issued_at__gte=seven_days_ago).count()
        
        return JsonResponse({
            'total_fines': total_fines,
            'total_revenue': str(total_revenue),
            'fines_paid': fines_paid,
            'revenue_collected': str(revenue_collected),
            'fines_pending': total_fines - fines_paid,
            'fines_this_week': fines_this_week,
            'pending_amount': str(total_revenue - revenue_collected),
        }, status=200)
    
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)