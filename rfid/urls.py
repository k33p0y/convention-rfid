from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # home page
    path('convention/create/', views.convention_create, name='convention_create'), # create new convention
    path('convention/<uuid:convention_id>/register/participant/', views.register_participant, name='register_participant'), # register participant
    path('convention/<uuid:convention_id>/register/existing/participant/', views.load_existing_participant_register_page, name='load_existing_participant_register_page'), # register existing participant
    path('convention/<uuid:convention_id>/register/existing/participant/<str:rfid_num>/', views.register_existing_participant, name='register_existing_participant'),
    path('check/participant/<str:rfid_num>/', views.check_rfid, name='check_rfid'), # check if rfid number is registered

    path('convention-list-json/', views.ConventionListJson.as_view(), name='convention_list_json'), # convention list json
    path('convention/list/', views.convention_list, name='convention_list'), # load convention list page
    path('convention/<uuid:convention_id>/', views.convention_view, name='convention_view'), # view convention details
    path('convention/<uuid:convention_id>/update/', views.convention_update, name='convention_update'), # update convention

    path('convention/<uuid:convention_id>/check-in/', views.load_check_in_page, name='load_check_in_page'), # load check-in page
    path('convention/<uuid:convention_id>/<str:rfid_num>/check-in/', views.log_attendance_check_in, name='log_attendance_check_in'), # log attendance check-in
    path('convention/<uuid:convention_id>/check-out/', views.load_check_out_page, name='load_check_out_page'), # load check-out page
    path('convention/<uuid:convention_id>/<str:rfid_num>/check-out/', views.log_attendance_check_out, name='log_attendance_check_out'), # log attendance check-out
    
    path('convention/<uuid:convention_id>/attendance/json/', views.generate_attendance_json, name='generate_attendance_json'), # get attendance json
    path('convention/<uuid:convention_id>/<str:rfid_num>/json/', views.get_participant_json, name='get_participant_json'), # get participant json, check if participant is registered to convention

    path('convention/<uuid:convention_id>/certificate/', views.load_certificate_generation_page, name='load_certificate_generation_page'), # load certificate generation page
    path('convention/<uuid:convention_id>/government-certificate/', views.load_government_certificate_generation_page, name='load_government_certificate_generation_page'), # load government certificate generation page
    path('convention/<uuid:convention_id>/id-card/', views.load_id_generation_page, name='load_id_generation_page'), # load id generation page

    path('participant-list-json/', views.ParticipantListJson.as_view(), name='participant_list_json'), # participant list json
    path('participant/list/', views.participant_list, name='participant_list'), # load participant list page
    path('participant/search/', views.load_participant_search_page, name='load_participant_search_page'), # load participant search page
    path('participant/search/<str:prc_num>/', views.participant_conventions_json, name='participant_conventions_json'), # participant convention list json

    # PRINT
    path('convention/<uuid:convention_id>/<str:rfid_num>/id/print/', views.print_id_card, name='print_id_card'), # print id card (html hard-coded)
    path('convention/<uuid:convention_id>/<str:rfid_num>/certificate/print/', views.print_certificate, name='print_certificate'), # print certificate (html hard-coded)
    path('convention/<uuid:convention_id>/<str:rfid_num>/certificate-government/print/', views.print_certificate_government, name='print_certificate_government'), # print government certificate (html hard-coded)
]