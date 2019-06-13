from django.urls import path
from . import views

# SOCIETY
urlpatterns = [
    path('society/', views.society_list, name='society_list'),
    path('society-list-json/', views.SocietyListJson.as_view(), name='society_list_json'),
]