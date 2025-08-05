from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import RegisterForm, ProfileForm
from .models import UserProfile
from tasks.forms import TeamLeaderRequestForm


def home(request):
    return render(request, 'common/home.html')


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('home')
    return render(request, 'common/register.html', {'form': form})


@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'common/profile.html', {'form': form})


@login_required
def team_leader_request_view(request):
    form = TeamLeaderRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        message = form.cleaned_data['message']
        subject = f"Заявка за Team Leader от {request.user.username}"
        body = (
            f"Потребител: {request.user.username}\n"
            f"Имейл: {request.user.email}\n\n"
            f"Съобщение:\n{message}"
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
        messages.success(request, "Заявката ти беше изпратена успешно!")
        return redirect('profile')
    return render(request, 'common/team_leader_request.html', {'form': form})

