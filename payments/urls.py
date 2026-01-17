from django.urls import path
from . import views

urlpatterns = [
    path(
        'tenacy/<int:tenancy_id>/rent-records',
        views.rent_record_list,
        name='rent_record_list'
    )
]