from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import EmailAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CaretakerCreationForm, UserProfileForm
from .models import User
from django.contrib import messages

# Create your views here.
@login_required
def my_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('my_profile')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'accounts/my_profile.html', {
        'form': form
    })

@login_required
def add_caretaker(request):
    if not request.user.is_landlord():
        return HttpResponseForbidden("You are not authorized to add a caretaker")
    
    if request.method == 'POST':
        form = CaretakerCreationForm(request.POST)
        if form.is_valid():
            caretaker = form.save(commit=False)
            caretaker.role = User.CARETAKER
            caretaker.set_password(form.cleaned_data['password1'])
            caretaker.save()
            messages.success(request, 'Caretaker created successfully')
            return redirect('landlord_dashboard')
    else:
        form = CaretakerCreationForm()
    
    return render(request, 'accounts/add_caretaker.html', {
        'form': form
    })

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