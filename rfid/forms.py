from django import forms
from .models import Participant, Rfid

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