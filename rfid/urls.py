from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('participant/register/', views.create_participant, name='create_participant'),
    path('participant/check-in/', views.participant_check_in, name='participant_check_in'),
    path('participant/<int:convention_id>/<str:rfid_num>/', views.log_attendance, name='log_attendance'),
]