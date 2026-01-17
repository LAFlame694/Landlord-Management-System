from django.urls import path
from . import views

urlpatterns = [
    path('', views.apartment_list, name='apartment_list'),
    path('add/', views.apartment_create, name='apartment_create'),
    path('<int:pk>/edit/', views.apartment_edit, name='apartment_edit'),
    path('caretaker/dashboard/', views.caretaker_dashboard, name='caretaker_dashboard'),
    path('<int:apartment_id>/units/', views.apartment_units, name='apartment_units'),
    path('<int:apartment_id>/units/add/', views.unit_create, name='unit_create'),
    path('vacate-tenant/<int:tenancy_id>/', views.vacate_tenant, name='vacate_tenant'),
    path('units/<unit_id>/assign-tenant', views.assign_tenant, name='assign_tenant')
]


