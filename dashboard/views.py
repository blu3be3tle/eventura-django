from django.shortcuts import render
from events.models import Event
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import AssignRoleForm, CreateGroupForm
from events.models import Event, Category
from django.db.models import Count


# Home
def home_view(request):
    return render(request, 'dashboard/home.html')


def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser


def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


@login_required
def dashboard(request):

    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    else:
        return redirect('participant-dashboard')


# Admin
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    now = timezone.now()
    today = now.date()

    total_users = User.objects.count()
    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    today_events_count = Event.objects.filter(date=today).count()
    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()

    current_filter = request.GET.get(
        'filter', 'users')

    context = {
        'total_users': total_users,
        'total_events': total_events,
        'total_categories': total_categories,
        'today_events_count': today_events_count,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'current_filter': current_filter,
    }

    if current_filter == 'users':
        context['users_to_display'] = User.objects.all(
        ).prefetch_related('groups')
    elif current_filter == 'categories':
        context['categories_to_display'] = Category.objects.all().annotate(
            event_count=Count('events'))
    else:
        events_query = Event.objects.select_related('category')
        if current_filter == 'past':
            events_query = events_query.filter(date__lt=today)
        elif current_filter == 'upcoming':
            events_query = events_query.filter(date__gte=today)
        elif current_filter == 'today':
            events_query = events_query.filter(date=today)

        context['events_to_display'] = events_query

    return render(request, 'dashboard/admin/admin_dashboard.html', context)


@user_passes_test(is_admin, login_url='login')
def manage_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()
            user.groups.add(role)
            messages.success(
                request, f"Role '{role.name}' assigned to {user.username}.")
            return redirect('admin-dashboard')
    else:
        initial_data = {'role': user.groups.first()}
        form = AssignRoleForm(initial=initial_data)

    return render(request, 'dashboard/admin/manage_user.html', {'form': form, 'user_to_manage': user})


@user_passes_test(is_admin, login_url='login')
def user_delete(request, pk):
    user_to_delete = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('admin-dashboard')

    context = {
        'user_to_delete': user_to_delete
    }
    return render(request, 'dashboard/admin/user_delete.html', context)


@user_passes_test(is_admin, login_url='login')
def group_list(request):
    groups = Group.objects.all().prefetch_related('permissions')
    return render(request, 'dashboard/admin/group_list.html', {'groups': groups})


@user_passes_test(is_admin, login_url='login')
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(
                request, f"Group '{group.name}' created successfully.")
            return redirect('group-list')
    else:
        form = CreateGroupForm()
    return render(request, 'dashboard/admin/create_group.html', {'form': form})


# Organizer
@user_passes_test(is_organizer, login_url='login')
def organizer_dashboard(request):
    now = timezone.now()
    today = now.date()

    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()

    current_filter = request.GET.get(
        'filter', 'upcoming')

    context = {
        'total_events': total_events,
        'total_categories': total_categories,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'current_filter': current_filter,
    }

    if current_filter == 'categories':
        context['categories_to_display'] = Category.objects.all().annotate(
            event_count=Count('events'))
    else:
        events_query = Event.objects.select_related('category')
        if current_filter == 'past':
            events_query = events_query.filter(date__lt=today)
        elif current_filter == 'upcoming':
            events_query = events_query.filter(date__gte=today)
        context['events_to_display'] = events_query

    return render(request, 'dashboard/organizer_dashboard.html', context)


# Participant
@login_required
def participant_dashboard(request):
    rsvpd_events = Event.objects.filter(
        users=request.user).order_by('date', 'time')

    context = {
        'rsvpd_events': rsvpd_events,
    }
    return render(request, 'dashboard/participant/participant_dashboard.html', context)
