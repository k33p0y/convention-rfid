from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('convention/<uuid:convention_id>/register/participant/', views.register_participant, name='register_participant'),
    path('convention/<uuid:convention_id>/check-in/', views.participant_check_in, name='participant_check_in'), # load check-in page
    path('convention/<uuid:convention_id>/check-out/', views.participant_check_out, name='participant_check_out'), # load check-out page
    path('convention/<uuid:convention_id>/<str:rfid_num>/check-in/', views.log_attendance_check_in, name='log_attendance_check_in'), # log attendance check-in
    path('convention/<uuid:convention_id>/<str:rfid_num>/check-out/', views.log_attendance_check_out, name='log_attendance_check_out'), # log attendance check-out
]

urlpatterns += [
    path('convention-list-json/', views.ConventionListJson.as_view(), name='convention_list_json'),
    path('convention/list/', views.convention_list, name='convention_list'),
    path('convention/<uuid:convention_id>/', views.convention_view, name='convention_view'),
]