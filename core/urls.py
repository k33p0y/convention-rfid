from django.urls import path
from . import views

# SOCIETY
urlpatterns = [
    path('society/', views.society_list, name='society_list'),
    path('society-list-json/', views.SocietyListJson.as_view(), name='society_list_json'),
    path('society/create/', views.society_create, name='society_create'),
    path('society/<uuid:uuid>/update/', views.society_update, name='society_update'),
]

# MEMBERSHIP
urlpatterns += [
    path('membership/', views.membership_list, name='membership_list'),
    path('membership-list-json/', views.MembershipListJson.as_view(), name='membership_list_json'),
    path('membership/create/', views.membership_create, name='membership_create'),
    path('membership/<uuid:uuid>/update/', views.membership_update, name='membership_update'),
]

# PARTICIPANT
urlpatterns += [
    path('participant/', views.participant_list, name='participant_list'),
    path('participant-list-json/', views.ParticipantListJson.as_view(), name='participant_list_json'),
    path('participant/create/', views.participant_create, name='participant_create'),
    path('participant/<uuid:uuid>/update/', views.participant_update, name='participant_update'),
]

# CONVENTION
urlpatterns += [
    path('list/', views.convention_list, name='convention_list'),
    path('list-json/', views.ConventionListJson.as_view(), name='convention_list_json'),
    path('create/', views.convention_create, name='convention_create'),
    path('<uuid:uuid>/update/', views.convention_update, name='convention_update'),
]