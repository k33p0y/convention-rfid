import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime
from django_datatables_view.base_datatable_view import BaseDatatableView
from .models import Participant, Convention, Society, Membership, Rfid, Attendance
from .forms import SocietyForm, MembershipForm, ParticipantForm, ConventionForm, RfidForm

# Generic form save
def save_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
    
def home(request):
    return render(request, 'index.html', {})

# SOCIETY START
class SocietyListJson(BaseDatatableView):
    model = Society
    columns = ['name', 'date_created', 'date_updated', 'action']
    order_columns = ['name', 'date_created', 'date_updated', '']

    # exclude is_archived = True in datatables
    def get_initial_queryset(self):
        return Society.objects.all()
    
    def get_filter_method(self):
        """ Returns preferred filter method """
        return self.FILTER_ICONTAINS

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)

        if search:
            qs = qs.filter(name__icontains=search)
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return """
                <button class='btn btn-default m-0 p-0 js-update-society' data-url='/convention/society/%s/update/' data-toggle='tooltip' title='Update'>
                    <i class='far fa-edit text-primary'></i>
                </button>
            """ % (row.society_id) # create action buttons
        elif column == 'date_created':
            return "%s" % localtime(row.date_created).strftime("%Y-%m-%d %H:%M") # format date_created to "YYYY-MM-DD HH:mm"
        elif column == 'date_updated':
            # return "%s" % row.date_updated.strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
            return "%s" % localtime(row.date_updated).strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
        else:
            return super(SocietyListJson, self).render_column(row, column)

def society_list(request):
    return render(request, 'core/society_list.html', {})

def society_create(request):
    if request.method == 'POST':
        form = SocietyForm(request.POST)
    else:
        form = SocietyForm()
    return save_form(request, form, 'core/society/partial_society_create.html')

def society_update(request, uuid):
    society = get_object_or_404(Society, society_id=uuid)
    if request.method == 'POST':
        form = SocietyForm(request.POST, instance=society)
    else:
        form = SocietyForm(instance=society)
    return save_form(request, form, 'core/society/partial_society_update.html')
# SOCIETY END

# MEMBERSHIP START
class MembershipListJson(BaseDatatableView):
    model = Membership
    columns = ['name', 'date_created', 'date_updated', 'action']
    order_columns = ['name', 'date_created', 'date_updated', '']

    # exclude is_archived = True in datatables
    def get_initial_queryset(self):
        return Membership.objects.all()
    
    def get_filter_method(self):
        """ Returns preferred filter method """
        return self.FILTER_ICONTAINS

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)

        if search:
            qs = qs.filter(name__icontains=search)
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return """
                <button class='btn btn-default m-0 p-0 js-update-membership' data-url='/convention/membership/%s/update/' data-toggle='tooltip' title='Update'>
                    <i class='far fa-edit text-primary'></i>
                </button>
            """ % (row.membership_id) # create action buttons
        elif column == 'date_created':
            return "%s" % localtime(row.date_created).strftime("%Y-%m-%d %H:%M") # format date_created to "YYYY-MM-DD HH:mm"
        elif column == 'date_updated':
            # return "%s" % row.date_updated.strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
            return "%s" % localtime(row.date_updated).strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
        else:
            return super(MembershipListJson, self).render_column(row, column)

def membership_list(request):
    return render(request, 'core/membership_list.html', {})

def membership_create(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)
    else:
        form = MembershipForm()
    return save_form(request, form, 'core/membership/partial_membership_create.html')

def membership_update(request, uuid):
    membership = get_object_or_404(Membership, membership_id=uuid)
    if request.method == 'POST':
        form = MembershipForm(request.POST, instance=membership)
    else:
        form = MembershipForm(instance=membership)
    return save_form(request, form, 'core/membership/partial_membership_update.html')
# MEMBERSHIP END

# PARTICIPANT START
class ParticipantListJson(BaseDatatableView):
    model = Participant
    columns = ['fname', 'mname', 'lname', 'prc_num', 'birthdate', 'address', 'date_created', 'date_updated', 'action']
    order_columns = ['fname', 'mname', 'lname', 'prc_num', 'birthdate', 'address', 'date_created', 'date_updated', '']

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
                q = Q(fname__icontains=part)|Q(mname__icontains=part)|Q(lname__icontains=part)|Q(address__icontains=part)|Q(prc_num__icontains=part)|Q(birthdate__icontains=part)|Q(address__icontains=part)
                qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return """
                <button class='btn btn-default m-0 p-0 js-update-participant' data-url='/convention/participant/%s/update/' data-toggle='tooltip' title='Update'>
                    <i class='far fa-edit text-primary'></i>
                </button>
                <a class='btn btn-default m-0 p-0 js-view-cost-center' href='/convention/participant/%s/view-details/' data-toggle='tooltip' title='View Details'>
                    <i class='far fa-eye text-primary'></i>
                </a>
            """ % (row.participant_id, row.participant_id) # create action buttons
        elif column == 'date_created':
            return "%s" % localtime(row.date_created).strftime("%Y-%m-%d %H:%M") # format date_created to "YYYY-MM-DD HH:mm"
        elif column == 'date_updated':
            # return "%s" % row.date_updated.strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
            return "%s" % localtime(row.date_updated).strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
        else:
            return super(ParticipantListJson, self).render_column(row, column)

def participant_list(request):
    return render(request, 'core/participant_list.html', {})

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
    else:
        form = ParticipantForm()
    return save_form(request, form, 'core/participant/partial_participant_create.html')

def participant_update(request, uuid):
    participant = get_object_or_404(Participant, participant_id=uuid)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
    else:
        form = ParticipantForm(instance=participant)
    return save_form(request, form, 'core/participant/partial_participant_update.html')

def participant_view_details(request, uuid):
    participant = get_object_or_404(Participant, participant_id=uuid)
    rfids = participant.rfid_set.select_related('society', 'membership', 'participant').all()
    context = {
        'participant': participant,
    }
    return render(request, 'core/participant/view_details.html', context)
# PARTICIPANT END

# CONVENTION START
class ConventionListJson(BaseDatatableView):
    model = Convention
    columns = ['name', 'date_start', 'date_end', 'society', 'date_created', 'date_updated', 'action']
    order_columns = ['name', 'date_start', 'date_end', 'society', 'date_created', 'date_updated', '']

    # exclude is_archived = True in datatables
    def get_initial_queryset(self):
        return Convention.objects.all()
    
    def get_filter_method(self):
        """ Returns preferred filter method """
        return self.FILTER_ICONTAINS

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)

        if search:
            search_parts = search.split(' ')
            qs_params = None
            for part in search_parts:
                q = Q(name__icontains=part)|Q(date_start__icontains=part)|Q(date_end__icontains=part)|Q(society__name__icontains=part)
                qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

    def render_column(self, row, column):
        if column == 'action':
            # set open/close icon and tooltip
            if row.is_open:
                icon = '<i class="fas fa-lock-open text-primary"></i>'
                tooltip = 'Close'
            else:
                icon = '<i class="fas fa-lock text-danger"></i>'
                tooltip = 'Open'

            return """
                <button class='btn btn-default m-0 p-0 js-update-convention' data-url='/convention/%s/update/' data-toggle='tooltip' title='Update'>
                    <i class='far fa-edit text-primary'></i>
                </button>
                <a class='btn btn-default m-0 p-0' href='/convention/%s/' data-toggle='tooltip' title='Attendance'>
                    <i class="fas fa-stopwatch text-primary"></i>
                </a>
                <button class='btn btn-default m-0 p-0 js-open-close-convention' data-url='/convention/%s/toggle/open-close/' data-toggle='tooltip' title='%s'>
                    %s
                </button>
            """ % (row.convention_id, row.convention_id, row.convention_id, tooltip, icon) # create action buttons
        elif column == 'date_created':
            return "%s" % localtime(row.date_created).strftime("%Y-%m-%d %H:%M") # format date_created to "YYYY-MM-DD HH:mm"
        elif column == 'date_updated':
            # return "%s" % row.date_updated.strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
            return "%s" % localtime(row.date_updated).strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
        else:
            return super(ConventionListJson, self).render_column(row, column)

def convention_list(request):
    return render(request, 'core/convention_list.html', {})

def convention_create(request):
    if request.method == 'POST':
        form = ConventionForm(request.POST)
    else:
        form = ConventionForm()
    return save_form(request, form, 'core/convention/partial_convention_create.html')

def convention_update(request, uuid):
    convention = get_object_or_404(Convention, convention_id=uuid)
    if request.method == 'POST':
        form = ConventionForm(request.POST, instance=convention)
    else:
        form = ConventionForm(instance=convention)
    return save_form(request, form, 'core/convention/partial_convention_update.html')

def toggle_convention_open_close(request, uuid):
    data = dict()
    convention = get_object_or_404(Convention, convention_id=uuid)

    if request.method == 'POST':
        if convention.is_open:
            convention.is_open = False
            convention.save()
        else:
            # Convention.objects.filter(is_open=True).update(is_open=False)
            convention.is_open = True
            convention.save()
        data['form_is_valid'] = True
    else:
        data['name'] = convention.name
        data['is_open'] = convention.is_open

    context = {'convention': convention}
    template_name = 'core/convention/partial_convention_toggle_open_close.html'
    data['html_form'] = render_to_string(template_name, context, request)
    return JsonResponse(data)
# CONVENTION END

# RFID START
def get_rfids_json(request, uuid):
    participant = get_object_or_404(Participant, participant_id=uuid)
    rfids = participant.rfid_set.select_related('society', 'membership').values('rfid_uuid', 'rfid_num', 'society__name', 'membership__name', 'date_created', 'date_updated')

    return JsonResponse(list(rfids), safe=False)

def rfid_create(request):
    data = dict()
    if request.method == 'POST':
        form = RfidForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            # get participant
            participant_id = request.POST['participant_id']
            participant = Participant.objects.get(participant_id=participant_id)
            
            obj.participant = participant
            obj.save()

            # get all rfids of partipant
            rfids = participant.rfid_set.select_related('society', 'membership').values('rfid_uuid', 'rfid_num', 'society__name', 'membership__name', 'date_created', 'date_updated')
            data['form_is_valid'] = True
            data['rfids'] = list(rfids)
        else:
            data['form_is_valid'] = False
    else:
        form = RfidForm()
    context = {'form': form}
    template_name = 'core/rfid/partial_rfid_create.html'
    data['html_form'] = render_to_string(template_name, context, request)

    return JsonResponse(data)

def rfid_update(request, uuid):
    data = dict()
    rfid = get_object_or_404(Rfid, rfid_uuid=uuid)
    if request.method == 'POST':
        form = RfidForm(request.POST, instance=rfid)
        if form.is_valid():
            obj = form.save()

            # get participant
            participant = Participant.objects.get(participant_id=obj.participant.participant_id)
            
            # get rfids all rfids of participant
            rfids = participant.rfid_set.select_related('society', 'membership').values('rfid_uuid', 'rfid_num', 'society__name', 'membership__name', 'date_created', 'date_updated')
            
            data['form_is_valid'] = True
            data['rfids'] = list(rfids)
        else:
            data['form_is_valid'] = False
    else:
        form = RfidForm(instance=rfid)

    context = {'form': form}
    template_name = 'core/rfid/partial_rfid_update.html'
    data['html_form'] = render_to_string(template_name, context, request)

    return JsonResponse(data)
# RFID END

# ATTENDANCE START
def participant_attendance(request, convention_uuid):
    convention = get_object_or_404(Convention, convention_id=convention_uuid)
    registered_participants = Rfid.objects.filter(society=convention.society).count()
    checked_in_participants = Attendance.objects.filter(convention=convention).values('rfid').distinct().count()

    context = {
        'convention': convention,
        'registered_participants': registered_participants,
        'checked_in_participants': checked_in_participants
    }
    return render(request, 'core/attendance/attendance.html', context)

@csrf_exempt
def create_or_update_attendance(request, convention_uuid):
    data = dict()
    convention = get_object_or_404(Convention, convention_id=convention_uuid)
    # get rfid from post form
    rfid_post = request.POST.get('rfid')

    # check if participant is registered to the convention
    try:
        rfid = Rfid.objects.get(society=convention.society.society_id, rfid_num__iexact=rfid_post)
        data['rfid'] = True

        # check if participant attendance exists
        try:
            attendance = Attendance.objects.get(rfid=rfid,
                convention=convention,
                date_created__year=datetime.datetime.now().year,
                date_created__month=datetime.datetime.now().month,
                date_created__day=datetime.datetime.now().day)

            # if convention is closed, set attendance.check_out to current time
            if convention.is_open == False and attendance.check_out == None:
                attendance.check_out = datetime.datetime.now().time()
                attendance.save()
                data['convention_is_open'] = False
            elif convention.is_open:
                data['convention_is_open'] = True
            data['participant']= participant_json(attendance)
        
        # participant attendance does not exist, create attendance
        except Attendance.DoesNotExist:
            attendance = Attendance(rfid=rfid, convention=convention)
            attendance.save()
            data['convention_is_open'] = True   
            data['participant']= participant_json(attendance)
    
    # participant is not registered
    except Rfid.DoesNotExist:
        data['rfid'] = False

    return JsonResponse(data)

def participant_json(obj):
    participant = {
        'attendance_uuid': obj.attendance_id,
        'rfid_num': obj.rfid.rfid_num,
        'fname': obj.rfid.participant.fname,
        'mname': obj.rfid.participant.mname,
        'lname': obj.rfid.participant.lname,
    }
    return participant

def get_participant_count_json(request, convention_uuid):
    data = dict()
    convention = get_object_or_404(Convention, convention_id=convention_uuid)
    registered_participants = Rfid.objects.filter(society=convention.society).count()
    checked_in_participants = Attendance.objects.filter(convention=convention).values('rfid').distinct().count()
    data['convention_is_open'] = convention.is_open
    data['registered_participants'] = registered_participants
    data['checked_in_participants'] = checked_in_participants
    return JsonResponse(data)

def generate_attendance_json(request, convention_uuid):
    convention = get_object_or_404(Convention, convention_id=convention_uuid)
    attendance = Attendance.objects.select_related('rfid__participant', 'convention').filter(convention=convention).values(
        'rfid__participant__fname', 'rfid__participant__mname', 'rfid__participant__lname', 'rfid__participant__prc_num', 'check_in', 'check_out', 'date_created'
    )

    attendance_list = list(attendance)
    return JsonResponse(attendance_list, safe=False)
# ATTENDANCE END