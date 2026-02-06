from django.urls import path
from . import views
from .views import landlord_dashboard, caretaker_dashboard

urlpatterns = [
    path('landlord/', landlord_dashboard, name='landlord_dashboard'),
    path('caretaker/', caretaker_dashboard, name='caretaker_dashboard'),
    path('home/', views.home_redirect, name='home')
]