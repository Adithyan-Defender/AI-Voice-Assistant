from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import CustomUser
import random
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

# ------------------------
# OTP EMAIL SENDER
# ------------------------
@csrf_exempt  # Optional: better if you use proper CSRF handling
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)

        otp = str(random.randint(100000, 999999))

        # Store OTP and email in session
        request.session['otp'] = otp
        request.session['email'] = email

        # Optional: Send the OTP via email
        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP code is: {otp}',
            from_email='your@email.com',
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)
# ------------------------
# REGISTRATION VIEW
# ------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request=request)  # pass request here
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password1'])
            user.save()

            login(request, user)
            request.session.pop('otp', None)
            request.session.pop('email', None)
            return redirect('accounts:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm(request=request)
    return render(request, 'screens/register.html', {'form': form})

# ------------------------
# LOGIN VIEW
# ------------------------
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('web:home')  # Ensure this URL name exists
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'screens/login.html', {'form': form})

# ------------------------
# LOGOUT VIEW
# ------------------------

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('accounts:login')

# ------------------------
# PASSWORD RESET VIEW
# ------------------------
def password_reset_view(request):
    session_otp = request.session.get('reset_otp')
    session_email = request.session.get('reset_email')

    if request.method == 'POST':
        if not session_otp:
            # Step 1: Send OTP
            email = request.POST.get('email')
            if CustomUser.objects.filter(email=email).exists():
                otp = str(random.randint(100000, 999999))
                request.session['reset_otp'] = otp
                request.session['reset_email'] = email

                subject = "Password Reset OTP"
                message = f"Your password reset code is: {otp}"

                try:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                    messages.success(request, "OTP sent to your email.")
                except Exception as e:
                    print(e)
                    messages.error(request, "Failed to send OTP. Try again.")
            else:
                messages.error(request, "No account found with this email.")
        else:
            # Step 2: Verify OTP and Reset Password
            otp = request.POST.get('otp')
            new_password = request.POST.get('password1')
            confirm_password = request.POST.get('password2')

            if otp != session_otp:
                messages.error(request, "Invalid OTP.")
            elif new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
            elif len(new_password) < 6:
                messages.error(request, "Password must be at least 6 characters.")
            else:
                try:
                    user = CustomUser.objects.get(email=session_email)
                    user.set_password(new_password)
                    user.save()
                    request.session.pop('reset_otp', None)
                    request.session.pop('reset_email', None)
                    messages.success(request, "Password reset successful. Please login.")
                    return redirect('accounts:login')
                except CustomUser.DoesNotExist:
                    messages.error(request, "User not found.")

    return render(request, 'screens/password_reset.html')




@login_required
def profile_view(request):
    return render(request, 'screens/profile.html', {'user': request.user})
