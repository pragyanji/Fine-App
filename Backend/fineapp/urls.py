from django.urls import path
from . import views

urlpatterns = [
    # API endpoints will be added here
    path('api/fine/', views.fine_list, name='fine-list'),
]