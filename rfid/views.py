from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Convention
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

def participant_check_in(request):
    convention = get_object_or_404(Convention, is_open=True)
    
    template_name = 'rfid/participant_check_in.html'
    context = {
        
    }
    return render(request, template_name, context)
