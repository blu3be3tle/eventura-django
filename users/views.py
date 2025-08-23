from .forms import EditProfileForm, EditProfilePictureForm, CustomPasswordChangeForm, SignUpForm, LoginForm
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator


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


# Profile
class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'profile/profile.html')


class EditProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        profile_form = EditProfileForm(instance=request.user)
        picture_form = EditProfilePictureForm(instance=request.user.profile)
        context = {
            'profile_form': profile_form,
            'picture_form': picture_form,
        }
        return render(request, 'profile/edit_profile.html', context)

    def post(self, request, *args, **kwargs):
        profile_form = EditProfileForm(request.POST, instance=request.user)
        picture_form = EditProfilePictureForm(
            request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and picture_form.is_valid():
            profile_form.save()
            picture_form.save()
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('profile')

        context = {
            'profile_form': profile_form,
            'picture_form': picture_form,
        }
        return render(request, 'profile/edit_profile.html', context)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):

    form_class = CustomPasswordChangeForm
    template_name = 'users/profile/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(
            self.request, 'Your password was successfully updated!')
        return super().form_valid(form)
