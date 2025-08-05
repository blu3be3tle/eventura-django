from django.shortcuts import render
from .models import Participant
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q

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

