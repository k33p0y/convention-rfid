from django.urls import path
from . import views

urlpatterns = [
    path('society/', views.society_list, name='society_list'),
]