from django.urls import path
from . import views

urlpatterns = [
    # Fine endpoints
    path('api/fines/create/', views.create_fine, name='fine-create'),
    path('api/fines/<int:fine_id>/', views.get_fine_details, name='fine-details'),
    path('api/fines/<int:fine_id>/status/', views.update_fine_status, name='fine-status-update'),
    
    # Vehicle endpoints
    path('api/vehicle/details/', views.vehicle_details, name='vehicle-details'),
    path('api/vehicle/<str:number_plate>/fines/', views.get_fines_by_vehicle, name='vehicle-fines'),
    
    # Statistics endpoints
    path('api/statistics/', views.get_statistics, name='statistics'),
]