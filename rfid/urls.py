from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('convention/<uuid:convention_id>/register/participant/', views.register_participant, name='register_participant'), # register participant

    path('convention-list-json/', views.ConventionListJson.as_view(), name='convention_list_json'), # convention list json
    path('convention/list/', views.convention_list, name='convention_list'), # load convention list page
    path('convention/<uuid:convention_id>/', views.convention_view, name='convention_view'), # view convention details

    path('convention/<uuid:convention_id>/check-in/', views.load_check_in_page, name='load_check_in_page'), # load check-in page
    path('convention/<uuid:convention_id>/<str:rfid_num>/check-in/', views.log_attendance_check_in, name='log_attendance_check_in'), # log attendance check-in
    path('convention/<uuid:convention_id>/check-out/', views.load_check_out_page, name='load_check_out_page'), # load check-out page
    path('convention/<uuid:convention_id>/<str:rfid_num>/check-out/', views.log_attendance_check_out, name='log_attendance_check_out'), # log attendance check-out
    
    path('convention/<uuid:convention_id>/attendance/json/', views.generate_attendance_json, name='generate_attendance_json'), # get attendance json
    path('convention/<uuid:convention_id>/<str:rfid_num>/json/', views.get_participant_json, name='get_participant_json'), # get participant json

    path('convention/<uuid:convention_id>/certificate/', views.load_certificate_generation_page, name='load_certificate_generation_page'), # load certificate generation page   
]