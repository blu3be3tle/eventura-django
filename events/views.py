from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = Participant.objects.filter(event=event)
    return render(request, 'events/event_detail.html', {'event': event, 'participants': participants})


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})
