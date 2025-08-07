from django.urls import path, include
from . import views


urlpatterns = [

    path('organizer-dashboard/', views.organizer_dashboard, name='dashboard'),
]
