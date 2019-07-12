from django.urls import path
from . import views

urlpatterns = [
    path('participant/register/', views.create_participant, name='create_participant'),
    path('participant/check-in/', views.participant_check_in, name='participant_check_in'),
]