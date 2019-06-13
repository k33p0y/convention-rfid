from django.urls import path
from . import views

# SOCIETY
urlpatterns = [
    path('society/', views.society_list, name='society_list'),
    path('society-list-json/', views.SocietyListJson.as_view(), name='society_list_json'),
    path('society/create/', views.society_create, name='society_create'),
    path('society/<uuid:uuid>/update/', views.society_update, name='society_update'),
]