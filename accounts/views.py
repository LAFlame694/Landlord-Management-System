from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import EmailAuthenticationForm

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm

    def get_success_url(self):
        user = self.request.user
        
        if user.is_landlord():
            return reverse_lazy('landlord_dashboard')
        elif user.is_caretaker():
            return reverse_lazy('caretaker_dashboard')
        return reverse_lazy('login')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')