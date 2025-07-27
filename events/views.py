from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import Event, Category, Participant
from .forms import EventForm
import datetime


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
    return render(request, 'event_app/event_list.html', context)


def event_detail(request, pk):

    event = get_object_or_404(
        Event.objects.select_related(
            'category').prefetch_related('participants'),
        pk=pk
    )
    context = {'event': event}
    return render(request, 'event_app/event_detail.html', context)


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    else:
        form = EventForm()
    context = {'form': form}
    return render(request, 'event_app/event_form.html', context)


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
    return render(request, 'event_app/event_form.html', context)


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event-list')
    context = {'event': event}
    return render(request, 'event_app/event_delete.html', context)
