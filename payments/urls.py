from django.urls import path
from . import views

urlpatterns = [
    path(
        'tenacy/<int:tenancy_id>/rent-records',
        views.rent_record_list,
        name='rent_record_list'
    ),

    path(
        'rent-record/<int:record_id>/pay',
        views.record_payment,
        name='record_payment'
    ),
]