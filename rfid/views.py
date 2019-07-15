from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Convention, Rfid, Attendance
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
        'convention': convention
    }
    return render(request, template_name, context)

def log_attendance(request, convention_id, rfid_num):
    data = dict()
    convention = get_object_or_404(Convention, id=convention_id)
    # rfids = convention.rfids.select_related('participant').all()
    if convention.rfids.filter(rfid_num=rfid_num).exists():
        data['participant_exist'] = True
        rfid = get_object_or_404(Rfid, rfid_num=rfid_num)
        attendance_obj = Attendance(convention=convention, rfid=rfid)
        attendance_obj.save()

        data['participant_name'] = rfid.participant.fname + ' ' + rfid.participant.lname
    else:
        data['participant_exist'] = False
    
    return JsonResponse(data)