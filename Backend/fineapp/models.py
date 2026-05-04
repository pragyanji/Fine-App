from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

# Vehicle Model
class Vehicle(models.Model):
    """Store registered vehicle information"""
    VEHICLE_TYPES = [
        ('Motorcycle', 'Motorcycle'),
        ('Car', 'Car'),
        ('Bus', 'Bus'),
        ('Truck', 'Truck'),
        ('Auto-rickshaw', 'Auto-rickshaw'),
        ('Scooter', 'Scooter'),
        ('Taxi', 'Taxi'),
        ('Other', 'Other'),
    ]
    
    number_plate = models.CharField(
        max_length=20, 
        unique=True, 
        db_index=True,
        help_text="Vehicle registration number plate (e.g., BA 1234 AB)"
    )
    vehicle_type = models.CharField(
        max_length=50, 
        choices=VEHICLE_TYPES
    )
    vehicle_model = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Vehicle make and model (e.g., Toyota Fortuner)"
    )
    vehicle_number = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Vehicle engine/chassis number"
    )
    owner_name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Registered owner's name"
    )
    owner_phone = models.CharField(
        max_length=15,
        help_text="Owner's phone number for notifications"
    )
    owner_address = models.TextField(
        blank=True,
        help_text="Owner's registered address"
    )
    registration_date = models.DateField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Vehicles"
    
    def __str__(self):
        return f"{self.number_plate} - {self.owner_name}"


# Violation Type Model
class ViolationType(models.Model):
    """Categories of traffic violations"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    default_fine_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    severity = models.CharField(
        max_length=20,
        choices=[
            ('Minor', 'Minor'),
            ('Moderate', 'Moderate'),
            ('Severe', 'Severe'),
        ],
        default='Moderate'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (₹{self.default_fine_amount})"


# Fine Model
class Fine(models.Model):
    """Store issued fines"""
    STATUS_CHOICES = [
        ('Issued', 'Issued'),
        ('Notified', 'Notified'),
        ('Acknowledged', 'Acknowledged'),
        ('Paid', 'Paid'),
        ('Disputed', 'Disputed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    # Vehicle and violator info
    vehicle = models.ForeignKey(
        Vehicle, 
        on_delete=models.PROTECT,
        related_name='fines'
    )
    
    # Officer info
    issued_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='issued_fines',
        help_text="Police officer who issued the fine"
    )
    
    # Violation details
    violation_type = models.ForeignKey(
        ViolationType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fines'
    )
    violation_explanation = models.TextField(
        help_text="Detailed description of the traffic violation"
    )
    violation_date = models.DateTimeField(
        help_text="Date and time of violation"
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Location where violation occurred"
    )
    
    # Fine amount
    fine_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Fine amount in rupees"
    )
    
    # Photo proof
    photo_proof = models.ImageField(
        upload_to='fine_proofs/%Y/%m/%d/',
        help_text="Photo evidence of the violation"
    )
    
    # Status and tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Issued'
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    notification_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When notification was sent to vehicle owner"
    )
    acknowledged_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When violator acknowledged the fine"
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When fine was paid"
    )
    
    # Additional notes
    notes = models.TextField(
        blank=True,
        help_text="Additional notes or comments"
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issued_at']
        indexes = [
            models.Index(fields=['vehicle', '-issued_at']),
            models.Index(fields=['status', '-issued_at']),
            models.Index(fields=['issued_by', '-issued_at']),
        ]
    
    def __str__(self):
        return f"Fine {self.id} - {self.vehicle.number_plate} (₹{self.fine_amount})"
    
    def mark_notified(self):
        """Mark fine as notified"""
        self.status = 'Notified'
        self.notification_sent_at = timezone.now()
        self.save(update_fields=['status', 'notification_sent_at'])
    
    def mark_paid(self):
        """Mark fine as paid"""
        self.status = 'Paid'
        self.paid_at = timezone.now()
        self.save(update_fields=['status', 'paid_at'])


# Notification Log Model
class NotificationLog(models.Model):
    """Track notifications sent to vehicle owners"""
    NOTIFICATION_TYPE_CHOICES = [
        ('SMS', 'SMS'),
        ('Email', 'Email'),
        ('App', 'App Notification (Nagarik)'),
        ('WhatsApp', 'WhatsApp'),
    ]
    
    fine = models.ForeignKey(
        Fine,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='App'
    )
    recipient = models.CharField(
        max_length=150,
        help_text="Phone number, email, or user ID"
    )
    message = models.TextField(
        help_text="Notification message content"
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Sent', 'Sent'),
            ('Delivered', 'Delivered'),
            ('Failed', 'Failed'),
        ],
        default='Pending'
    )
    response = models.TextField(
        blank=True,
        help_text="Response from notification service"
    )
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name_plural = "Notification Logs"
    
    def __str__(self):
        return f"{self.notification_type} - {self.recipient} ({self.status})"


# Police Officer Profile Model
class PoliceOfficer(models.Model):
    """Extended profile for police officers"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='police_officer'
    )
    badge_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Officer's badge/ID number"
    )
    department = models.CharField(
        max_length=150,
        blank=True,
        help_text="Police department/station"
    )
    designation = models.CharField(
        max_length=100,
        blank=True,
        help_text="Job title (e.g., Traffic Police, Constable)"
    )
    phone = models.CharField(
        max_length=15,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Police Officers"
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.badge_number})"
    
    @property
    def total_fines_issued(self):
        """Get total fines issued by this officer"""
        return self.user.issued_fines.count()


# Statistics Model (Optional - for caching stats)
class FineStatistics(models.Model):
    """Cache statistics for performance"""
    date = models.DateField(auto_now_add=True, unique=True)
    total_fines_issued = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    fines_paid = models.IntegerField(default=0)
    revenue_collected = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_notifications_sent = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Fine Statistics"
        ordering = ['-date']
    
    def __str__(self):
        return f"Statistics for {self.date}"
