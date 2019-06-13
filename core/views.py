from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils.timezone import localtime
from django_datatables_view.base_datatable_view import BaseDatatableView
from .models import Participant, Convention, Society, Membership
from .forms import SocietyForm, MembershipForm, ParticipantForm

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
    columns = ['rfid', 'fname', 'mname', 'lname', 'prc_num', 'birthdate', 'address', 'society', 'membership', 'date_created', 'date_updated', 'action']
    order_columns = ['rfid', 'fname', 'mname', 'lname', 'prc_num', 'birthdate', 'address', 'society', 'membership', 'date_created', 'date_updated', '']

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
                q = Q(rfid__icontains=part)|Q(fname__icontains=part)|Q(mname__icontains=part)|Q(lname__icontains=part)|Q(address__icontains=part)|Q(prc_num__icontains=part)|Q(birthdate__icontains=part)|Q(address__icontains=part)|Q(society__name__icontains=part)|Q(membership__name__icontains=part)  
                qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return """
                <button class='btn btn-default m-0 p-0 js-update-participant' data-url='/convention/participant/%s/update/' data-toggle='tooltip' title='Update'>
                    <i class='far fa-edit text-primary'></i>
                </button>
            """ % (row.membership_id) # create action buttons
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
# PARTICIPANT END