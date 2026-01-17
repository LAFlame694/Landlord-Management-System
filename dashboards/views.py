from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.utils import landlord_required, caretaker_required

# Create your views here.
@login_required
def landlord_dashboard(request):
    landlord_required(request.user)
    return render(request, 'dashboards/landlord_dashboard.html')

@login_required
def caretaker_dashboard(request):
    caretaker_required(request.user)
    return render(request, 'dashboards/caretaker_dashboard.html')