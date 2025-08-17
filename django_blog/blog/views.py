from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

# User Profile
@login_required
def profile(request):
    if request.method == 'POST':
        request.user.email = request.POST.get("email")
        request.user.save()
        return redirect('profile')
    return render(request, 'blog/profile.html')

# Login (built-in)
class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

# Logout (built-in)
class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'
