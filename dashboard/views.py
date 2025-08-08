from django.shortcuts import render
from events.models import Event
from django.utils import timezone
from users.models import User


# Home
def home_view(request):
    return render(request, 'dashboard/home.html')


# Dashboard
def organizer_dashboard(request):

    total_users = User.objects.count()
    total_events = Event.objects.count()

    now = timezone.now()
    upcoming_events_count = Event.objects.filter(date__gte=now.date()).count()
    past_events_count = Event.objects.filter(date__lt=now.date()).count()

    event_filter = request.GET.get('filter', 'upcoming')
    events_to_display = Event.objects.select_related('category')
    users_to_display = User.objects.none()

    if event_filter == 'users':
        users_to_display = User.objects.all()
    if event_filter == 'past':
        events_to_display = events_to_display.filter(date__lt=now.date())
    elif event_filter == 'today':
        events_to_display = events_to_display.filter(date=now.date())
    elif event_filter == 'upcoming':
        events_to_display = events_to_display.filter(date__gte=now.date())

    context = {
        'total_users': total_users,
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'today_events': Event.objects.filter(date=now.date()),
        'events_to_display': events_to_display,
        'users_to_display': users_to_display,
        'current_filter': event_filter,
    }
    return render(request, 'dashboard/organizer_dashboard.html', context)
