from django import forms
from .models import Participant, Rfid, Convention

class ParticipantForm(forms.ModelForm):
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 2},
        ),
    )
    birthdate = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date',},
        )
    )

    class Meta:
        model = Participant
        fields = ('fname', 'mname', 'lname', 'prc_num', 'birthdate', 'address', 'occupation')

class RfidForm(forms.ModelForm):
    class Meta:
        model = Rfid
        fields = ('rfid_num', 'society')

class ConventionForm(forms.ModelForm):
    date_start = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date',},
        )
    )
    date_end = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'type': 'date',},
        )
    )
    venue = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 2},
        ),
    )

    class Meta:
        model = Convention
        fields = ('name', 'is_open', 'date_start', 'date_end', 'venue',)