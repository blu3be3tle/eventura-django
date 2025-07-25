from django import forms
from .models import Event, Participant

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'category']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']