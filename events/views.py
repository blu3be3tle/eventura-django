from .forms import EventForm, ParticipantForm, CategoryForm
from .models import Event, Category, Participant
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone


# Event
def event_list(request):

    queryset = Event.objects.all()

    queryset = queryset.select_related('category').prefetch_related('participants').annotate(
        participant_count=Count('participants')
    )

    category_id = request.GET.get('category')
    if category_id:
        queryset = queryset.filter(category__id=category_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        queryset = queryset.filter(date__range=[start_date, end_date])

    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | Q(
                location__icontains=search_query)
        )

    categories = Category.objects.all()

    context = {
        'events': queryset,
        'categories': categories,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):

    event = get_object_or_404(
        Event.objects.select_related(
            'category').prefetch_related('participants'),
        pk=pk
    )
    context = {'event': event}
    return render(request, 'events/event_detail.html', context)


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    else:
        form = EventForm()
    context = {'form': form}
    return render(request, 'events/event_form.html', context)


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', pk=pk)
    else:
        form = EventForm(instance=event)
    context = {'form': form, 'event': event}
    return render(request, 'events/event_form.html', context)


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event-list')
    context = {'event': event}
    return render(request, 'events/event_delete.html', context)


# Dashboard
def organizer_dashboard(request):

    total_participants = Participant.objects.count()
    total_events = Event.objects.count()

    now = timezone.now()
    upcoming_events_count = Event.objects.filter(date__gte=now.date()).count()
    past_events_count = Event.objects.filter(date__lt=now.date()).count()

    event_filter = request.GET.get('filter', 'upcoming')
    events_to_display = Event.objects.select_related('category')

    if event_filter == 'past':
        events_to_display = events_to_display.filter(date__lt=now.date())
    elif event_filter == 'today':
        events_to_display = events_to_display.filter(date=now.date())
    elif event_filter == 'upcoming':
        events_to_display = events_to_display.filter(date__gte=now.date())

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'today_events': Event.objects.filter(date=now.date()),
        'events_to_display': events_to_display,
        'current_filter': event_filter,
    }
    return render(request, 'events/organizer_dashboard.html', context)


# Participant
def participant_list(request):
    participants = Participant.objects.all().prefetch_related('events')
    return render(request, 'participant/participant_list.html', {'participants': participants})


def participant_detail(request, pk):
    participant = get_object_or_404(
        Participant.objects.prefetch_related('events'), pk=pk)
    return render(request, 'participant/participant_detail.html', {'participant': participant})


def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            return redirect('participant-detail', pk=participant.pk)
    else:
        form = ParticipantForm()
    return render(request, 'participant/participant_form.html', {'form': form})


def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant-detail', pk=participant.pk)
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant/participant_form.html', {'form': form, 'participant': participant})


def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant-list')
    return render(request, 'participant/participant_delete.html', {'participant': participant})


# Category


def category_list(request):
    categories = Category.objects.all().annotate(event_count=Count('events'))
    context = {'categories': categories}
    return render(request, 'category/category_list.html', context)


def category_detail(request, pk):
    category = get_object_or_404(
        Category.objects.prefetch_related('events'),
        pk=pk
    )
    context = {'category': category}
    return render(request, 'category/category_detail.html', context)


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('category-detail', pk=category.pk)
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'category/category_form.html', context)


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    context = {'form': form, 'category': category}
    return render(request, 'category/category_form.html', context)


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    context = {'category': category}
    return render(request, 'category/category_delete.html', context)
