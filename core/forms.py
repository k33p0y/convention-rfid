from django import forms
from .models import Society, Membership, Convention, Participant

class SocietyForm(forms.ModelForm):
    class Meta:
        model = Society
        fields = ('name', )

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('name', )

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
        fields = ('rfid', 'fname', 'mname', 'lname', 'prc_num', 'birthdate', 'address', 'society', 'membership')