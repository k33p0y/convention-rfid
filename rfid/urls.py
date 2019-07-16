from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('convention/<uuid:convention_id>/register/participant/', views.register_participant, name='register_participant'),
    path('convention/<uuid:convention_id>/check-in/', views.participant_check_in, name='participant_check_in'),
    path('participant/<int:convention_id>/<str:rfid_num>/', views.log_attendance, name='log_attendance'),
]

urlpatterns += [
    path('convention-list-json/', views.ConventionListJson.as_view(), name='convention_list_json'),
    path('convention/list/', views.convention_list, name='convention_list'),
    path('convention/<uuid:convention_id>/', views.convention_view, name='convention_view'),
]