import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime
from django_datatables_view.base_datatable_view import BaseDatatableView
from .models import Convention, Rfid, Attendance, Participant, Occupation
from .forms import ParticipantForm, RfidForm, ConventionForm

def home(request):
    template_name = 'index.html'
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
    attendance = Attendance.objects.select_related('rfid__participant__occupation', 'convention').filter(convention=convention).values(
        'rfid__participant__fname', 'rfid__participant__mname', 'rfid__participant__lname', 'rfid__participant__prc_num', 'rfid__participant__occupation', 'rfid__participant__occupation__name', 'check_in', 'check_out', 'date_created'
    )

    attendance_list = list(attendance)
    for attendance in attendance_list:
        if attendance['check_in']:
            attendance['check_in'] = attendance['check_in'].strftime('%H:%M %p')
        if attendance['check_out']:
            attendance['check_out'] = attendance['check_out'].strftime('%H:%M %p')
    
    return JsonResponse(attendance_list, safe=False)

# get participant json
def get_participant_json(request, convention_id, rfid_num):
    data = dict()
    convention = get_object_or_404(Convention, id=convention_id)
    if convention.rfids.filter(rfid_num=rfid_num).exists():
        rfid = get_object_or_404(Rfid, rfid_num=rfid_num)

        data['participant_exist'] = True

        if rfid.participant.mname:
            data['participant_name'] = rfid.participant.fname + ' ' + rfid.participant.mname[0] + '. ' + rfid.participant.lname
        else:
            data['participant_name'] = rfid.participant.fname + ' ' + rfid.participant.lname

        data['prc_num'] = rfid.participant.prc_num
        data['occupation'] = rfid.participant.occupation.name
        data['initials'] = rfid.participant.occupation.initials
    else:
        data['participant_exist'] = False
    
    return JsonResponse(data)

# load certificate generation page
def load_certificate_generation_page(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)

    template_name = 'rfid/generate-certificate.html'
    context = {
        'convention': convention
    }
    return render(request, template_name, context)

# load government certificate generation page
def load_government_certificate_generation_page(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)

    template_name = 'rfid/generate-government-certificate.html'
    context = {
        'convention': convention
    }
    return render(request, template_name, context)

# load id generation page
def load_id_generation_page(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)

    template_name = 'rfid/generate-id.html'
    context = {
        'convention': convention
    }
    return render(request, template_name, context)

# participant list json
class ParticipantListJson(BaseDatatableView):
    model = Participant
    columns = ['prc_num', 'lname', 'fname', 'mname', 'birthdate', 'address', 'date_updated']
    order_columns = ['prc_num', 'lname', 'fname', 'mname', 'birthdate', 'address', 'date_updated']

    # exclude is_archived = True in datatables
    def get_initial_queryset(self):
        return Participant.objects.all()
    
    def get_filter_method(self):
        """ Returns preferred filter method """
        return self.FILTER_ICONTAINS

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)

        if search:
            search_parts = search.split(' ')
            qs_params = None
            for part in search_parts:
                q = Q(prc_num__icontains=part)|Q(lname__icontains=part)|Q(fname__icontains=part)|Q(mname__icontains=part)|Q(birthdate__icontains=part)|Q(address__icontains=part)
                qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

    def render_column(self, row, column):
        # if column == 'date_updated':
        #     return """
        #         <a class='btn btn-default m-0 p-0' href='/convention/%s/' target="_blank" data-toggle='tooltip' title='View'>
        #             <i class='far fa-eye text-primary'></i>
        #         </a>
        #     """ % (row.id) # create action buttons
        
        if column == 'birthdate':
            # return "%s" % row.date_updated.strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
            return "%s" % localtime(row.date_updated).strftime("%Y-%m-%d") # format date_updated to "YYYY-MM-DD HH:mm"
        elif column == 'date_updated':
            # return "%s" % row.date_updated.strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
            return "%s" % localtime(row.date_updated).strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
        else:
            return super(ParticipantListJson, self).render_column(row, column)

# load participant list page
def participant_list(request):
    return render(request, 'rfid/participant/participant-list.html', {})

# load participant search page
def load_participant_search_page(request):
    return render(request, 'rfid/participant/participant-search.html', {})

# participant convention list json
def participant_conventions_json(request, prc_num):
    data = dict()
    rfid = Rfid.objects.filter(participant__prc_num__exact=prc_num).first()
    if rfid:
        data['participant_exist'] = True
        participant = rfid
        conventions = rfid.convention_set.values('name', 'venue', 'date_start')

        data['conventions'] = list(conventions)
        data['participant_lname'] = rfid.participant.lname
        data['participant_fname'] = rfid.participant.fname
        data['participant_mname'] = rfid.participant.mname
        data['participant_prc_num'] = rfid.participant.prc_num
    else:
        data['participant_exist'] = False
    # data['test'] = True
    return JsonResponse(data, safe=False)

# load register page for existing participant
def load_existing_participant_register_page(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)

    context = {
        'convention': convention,
    }
    template_name = 'rfid/participant/participant-existing-register.html'
    return render(request, template_name, context)

# register existing participant to convention
@csrf_exempt
def register_existing_participant(request, convention_id, rfid_num):
    data = dict()
    convention = get_object_or_404(Convention, id=convention_id)
    if request.method == 'POST' and request.is_ajax():
        rfid_post_data = request.POST['rfid_num'] # get rfid post data
        rfid = Rfid.objects.filter(rfid_num__exact=rfid_post_data).first()
        if rfid:
            data['participant_exist'] = True
            if rfid.participant.mname:
                data['participant_name'] = rfid.participant.fname + ' ' + rfid.participant.mname[0] + '. ' + rfid.participant.lname
            else:
                data['participant_name'] = rfid.participant.fname + ' ' + rfid.participant.lname
            data['prc_num'] = rfid.participant.prc_num

            # add participant to convention
            convention.rfids.add(rfid)
        else:
            data['participant_exist'] = False

    return JsonResponse(data)

# check if rfid is registered
def check_rfid(request, rfid_num):
    data = dict()
    rfid = Rfid.objects.filter(rfid_num__exact=rfid_num).first()
    if rfid:
        data['rfid_exist'] = True
        if rfid.participant.mname:
            data['participant_name'] = rfid.participant.fname + ' ' + rfid.participant.mname[0] + '. ' + rfid.participant.lname
        else:
            data['participant_name'] = rfid.participant.fname + ' ' + rfid.participant.lname
        data['participant_prc_num'] = rfid.participant.prc_num
        data['rfid_num'] = rfid.rfid_num
    else:
        data['rfid_exist'] = False

    return JsonResponse(data)

# create convention
def convention_create(request):
    if request.method == 'POST':
        form = ConventionForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('convention_list')
    else:
        form = ConventionForm()
    template_name = 'rfid/convention/convention-create.html'
    context = {
        'form': form,
    }
    return render(request, template_name, context)

# update convention
def convention_update(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)

    if request.method == 'POST':
        form = ConventionForm(request.POST, instance=convention)
        if form.is_valid():
            obj = form.save()
            return redirect('convention_view', convention_id=convention.id)
    else:
        form = ConventionForm(instance=convention)
    template_name = 'rfid/convention/convention-update.html'
    context = {
        'form': form,
        'convention': convention,
    }
    return render(request, template_name, context)

# load print id card page
def print_id_card(request, convention_id, rfid_num):
    convention = get_object_or_404(Convention, id=convention_id)
    if convention.rfids.filter(rfid_num=rfid_num).exists():
        rfid = get_object_or_404(Rfid, rfid_num=rfid_num)
    else:
        rfid = None
    
    template_name = 'rfid/print-id.html'
    context = {
        'rfid': rfid,
    }
    return render(request, template_name, context)

# load print certificate page
def print_certificate(request, convention_id, rfid_num):
    convention = get_object_or_404(Convention, id=convention_id)
    if convention.rfids.filter(rfid_num=rfid_num).exists():
        rfid = get_object_or_404(Rfid, rfid_num=rfid_num)
    else:
        rfid = None
    
    template_name = 'rfid/print-certificate.html'
    context = {
        'rfid': rfid,
    }
    return render(request, template_name, context)

# load print government certificate page
def print_certificate_government(request, convention_id, rfid_num):
    convention = get_object_or_404(Convention, id=convention_id)
    if convention.rfids.filter(rfid_num=rfid_num).exists():
        rfid = get_object_or_404(Rfid, rfid_num=rfid_num)
    else:
        rfid = None
    
    template_name = 'rfid/print-certificate-government.html'
    context = {
        'rfid': rfid,
    }
    return render(request, template_name, context)

# load registered participants to convention page
def registered_participants_to_convention(request, convention_id):
    convention = get_object_or_404(Convention, id=convention_id)
    rfids = convention.rfids.select_related('participant__occupation').all
    
    template_name = 'rfid/participant/convention-participant-list.html'
    context = {
        'convention': convention,
        'rfids': rfids,
    }
    return render(request, template_name, context)