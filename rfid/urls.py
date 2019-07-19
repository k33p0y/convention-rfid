from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # home page
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
    path('convention/<uuid:convention_id>/id-card/', views.load_id_generation_page, name='load_id_generation_page'), # load certificate generation page

    path('participant-list-json/', views.ParticipantListJson.as_view(), name='participant_list_json'), # participant list json
    path('participant/list/', views.participant_list, name='participant_list'), # load participant list page
    path('participant/search/', views.load_participant_search_page, name='load_participant_search_page'), # load participant search page
    path('participant/search/<str:prc_num>/', views.participant_conventions_json, name='participant_conventions_json'), # participant convention list json
]