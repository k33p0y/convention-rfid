from django.urls import path
from . import views

urlpatterns = [
    path('participant/register/', views.create_participant, name='create_participant'),
]