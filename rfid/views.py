import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.utils.timezone import localtime
from django_datatables_view.base_datatable_view import BaseDatatableView
from .models import Convention, Rfid, Attendance
from .forms import ParticipantForm, RfidForm

def home(request):
    template_name = 'home.html'
    context ={}
    return render(request, template_name, context)

def register_participant(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)
    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        rfid_form = RfidForm(request.POST)
        if participant_form.is_valid() and rfid_form.is_valid():
            participant_obj = participant_form.save(commit=False)
            participant_obj.save()

            rfid_obj = rfid_form.save(commit=False)
            rfid_obj.participant = participant_obj
            rfid_obj.save()
            
            # associate rfid to convention
            convention.rfids.add(rfid_obj)

            messages.success(request, 'Participant %s %s saved to database!' % (participant_obj.fname, participant_obj.lname))
            return redirect('register_participant', convention_id=convention.id)
    else:
        participant_form = ParticipantForm()
        rfid_form = RfidForm()
    template_name = 'rfid/participant-create.html'
    context = {
        'participant_form': participant_form,
        'rfid_form': rfid_form,
        'convention': convention,
    }
    return render(request, template_name, context)

def load_check_in_page(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)
    
    template_name = 'rfid/attendance/attendance-check-in.html'
    context = {
        'convention': convention
    }
    return render(request, template_name, context)

def load_check_out_page(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)
    
    template_name = 'rfid/attendance/attendance-check-out.html'
    context = {
        'convention': convention
    }
    return render(request, template_name, context)

def log_attendance_check_in(request, convention_id, rfid_num):
    data = dict()
    convention = get_object_or_404(Convention, id=convention_id)
    # rfids = convention.rfids.select_related('participant').all()
    if convention.rfids.filter(rfid_num=rfid_num).exists():
        rfid = get_object_or_404(Rfid, rfid_num=rfid_num)
        
        try:
            attendance = Attendance.objects.get(convention=convention, rfid=rfid)

        except Attendance.DoesNotExist:
            attendance_obj = Attendance(convention=convention, rfid=rfid)
            attendance_obj.save()
        
        data['participant_exist'] = True
        data['participant_name'] = rfid.participant.fname + ' ' + rfid.participant.lname
    else:
        data['participant_exist'] = False
    
    return JsonResponse(data)

def log_attendance_check_out(request, convention_id, rfid_num):
    data = dict()
    convention = get_object_or_404(Convention, id=convention_id)
    # rfids = convention.rfids.select_related('participant').all()
    if convention.rfids.filter(rfid_num=rfid_num).exists():
        rfid = get_object_or_404(Rfid, rfid_num=rfid_num)
        
        try:
            attendance = Attendance.objects.get(convention=convention, rfid=rfid)
            if not attendance.check_out:
                attendance.check_out = datetime.datetime.now().time()
                attendance.save()
        
        except Attendance.DoesNotExist:
            attendance_obj = Attendance(convention=convention, rfid=rfid)
            attendance_obj.save()

        data['participant_exist'] = True
        data['participant_name'] = rfid.participant.fname + ' ' + rfid.participant.lname
    else:
        data['participant_exist'] = False
    
    return JsonResponse(data)

class ConventionListJson(BaseDatatableView):
    model = Convention
    columns = ['name', 'date_start', 'date_end', 'venue', 'date_updated', 'action']
    order_columns = ['name', 'date_start', 'date_start', 'venue', 'date_updated', '']

    # exclude is_archived = True in datatables
    def get_initial_queryset(self):
        if self.request.user.is_superuser:
            return Convention.objects.all()
        else:
            return Convention.objects.filter(is_open=True)
    
    def get_filter_method(self):
        """ Returns preferred filter method """
        return self.FILTER_ICONTAINS

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)

        if search:
            search_parts = search.split(' ')
            qs_params = None
            for part in search_parts:
                q = Q(name__icontains=part)|Q(venue__icontains=part)
                qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return """
                <a class='btn btn-default m-0 p-0' href='/convention/%s/' target="_blank" data-toggle='tooltip' title='View'>
                    <i class='far fa-eye text-primary'></i>
                </a>
            """ % (row.id) # create action buttons
        elif column == 'date_updated':
            # return "%s" % row.date_updated.strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
            return "%s" % localtime(row.date_updated).strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
        else:
            return super(ConventionListJson, self).render_column(row, column)

def convention_list(request):
    return render(request, 'rfid/convention/convention-list.html', {})

def convention_view(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)

    template_name = 'rfid/convention/convention-view.html'
    context = {
        'convention': convention,
    }
    return render(request, template_name, context)

def generate_attendance_json(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)
    attendance = Attendance.objects.select_related('rfid__participant', 'convention').filter(convention=convention).values(
        'rfid__participant__fname', 'rfid__participant__mname', 'rfid__participant__lname', 'rfid__participant__prc_num', 'check_in', 'check_out', 'date_created'
    )

    attendance_list = list(attendance)
    return JsonResponse(attendance_list, safe=False)