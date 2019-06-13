from django.shortcuts import render
from django.utils.timezone import localtime
from django_datatables_view.base_datatable_view import BaseDatatableView
from .models import Participant, Convention, Society, Membership

def home(request):
    return render(request, 'index.html', {})

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
                <button class='btn btn-default m-0 p-0' data-toggle='tooltip' title='Update'>
                    <i class='far fa-edit text-primary'></i>
                </button>
            """ # % (row.society_id) # create action buttons
        elif column == 'date_created':
            return "%s" % localtime(row.date_created).strftime("%Y-%m-%d %H:%M") # format date_created to "YYYY-MM-DD HH:mm"
        elif column == 'date_updated':
            # return "%s" % row.date_updated.strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
            return "%s" % localtime(row.date_updated).strftime("%Y-%m-%d %H:%M") # format date_updated to "YYYY-MM-DD HH:mm"
        else:
            return super(SocietyListJson, self).render_column(row, column)

def society_list(request):

    context = {
        
    }
    return render(request, 'core/society_list.html', context)