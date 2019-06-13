from django import forms
from .models import Society, Membership, Convention, Participant

class SocietyForm(forms.ModelForm):
    class Meta:
        model = Society
        fields = ('name', )