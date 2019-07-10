from django import forms
from .models import Society, Membership, Convention, Participant, Rfid

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
        fields = ('fname', 'mname', 'lname', 'prc_num', 'birthdate', 'address')
        # fields = ('rfid', 'fname', 'mname', 'lname', 'prc_num', 'birthdate', 'address', 'society', 'membership')

class ConventionForm(forms.ModelForm):
    date_start = forms.DateField(
        required=True,
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
        required=True,
        widget=forms.Textarea(
            attrs={'rows': 2},
        )
    )

    class Meta:
        model = Convention
        fields = ('name', 'date_start', 'date_end', 'society', 'venue')

class RfidForm(forms.ModelForm):
    class Meta:
        model = Rfid
        fields = ('rfid_num', 'society', 'membership')