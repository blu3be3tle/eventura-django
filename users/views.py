from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from users.forms import SignUpForm, LoginForm
from django.conf import settings

# Sign up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return render(request, 'registration/signup_success.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {"form": form})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event-list')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {"form": form})



def signout(request):
    logout(request)
    return redirect('login')



def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse('User not found')

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activation_success.html')
    else:
        return render(request, 'registration/activation_invalid.html')
