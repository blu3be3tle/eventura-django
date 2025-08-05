from django.shortcuts import render
from .models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .forms import UserForm

# User
def user_list(request):
    users = User.objects.all().prefetch_related('events')
    return render(request, 'user/user_list.html', {'users': users})


def user_detail(request, pk):
    user = get_object_or_404(
        User.objects.prefetch_related('events'), pk=pk)
    return render(request, 'user/user_detail.html', {'user': user})


def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user-detail', pk=user.pk)
    else:
        form = UserForm()
    return render(request, 'user/user_form.html', {'form': form})


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-detail', pk=user.pk)
    else:
        form = UserForm(instance=user)
    return render(request, 'user/user_form.html', {'form': form, 'user': user})


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user-list')
    return render(request, 'user/user_delete.html', {'user': user})

