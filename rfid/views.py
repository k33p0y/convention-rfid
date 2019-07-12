from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ParticipantForm, RfidForm

def create_participant(request):
    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        rfid_form = RfidForm(request.POST)
        if participant_form.is_valid() and rfid_form.is_valid():
            participant_obj = participant_form.save(commit=False)
            participant_obj.save()

            rfid_obj = rfid_form.save(commit=False)
            rfid_obj.participant = participant_obj
            rfid_obj.save()
            messages.success(request, 'Participant %s %s saved to database!' % (participant_obj.fname, participant_obj.lname))
            return redirect('create_participant')
    else:
        participant_form = ParticipantForm()
        rfid_form = RfidForm()
    template_name = 'rfid/participant_create.html'
    context = {
        'participant_form': participant_form,
        'rfid_form': rfid_form,
    }
    return render(request, template_name, context)