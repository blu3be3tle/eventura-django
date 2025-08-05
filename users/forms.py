from django import forms
from .models import Event, Participant


class ParticipantForm(forms.ModelForm):
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']