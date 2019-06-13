from django.shortcuts import render
from .models import Participant, Convention, Society, Membership

def home(request):
    return render(request, 'index.html', {})

def society_list(request):

    context = {
        
    }
    return render(request, 'core/society_list.html', context)