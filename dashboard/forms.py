from django.contrib.auth.models import Group, Permission
from django import forms

class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Select Role",
        empty_label="--Select Role--",
        widget=forms.Select(attrs={'class': 'mt-1 block w-full p-2 border border-gray-300 rounded-md'})
    )


class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permissions'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']