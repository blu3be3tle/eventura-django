from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.event_list, name='event-list'),
    path('event/<int:pk>/', views.event_detail, name='event-detail'),
    path('event/new/', views.event_create, name='event-create'),
    path('event/<int:pk>/edit/', views.event_update, name='event-update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event-delete'),
    path('organizer-dashboard/', views.organizer_dashboard, name='dashboard'),
    path("__reload__/", include("django_browser_reload.urls")),

    path('participants/', views.participant_list, name='participant-list'),
    path('participant/<int:pk>/', views.participant_detail,
         name='participant-detail'),
    path('participant/new/', views.participant_create, name='participant-create'),
    path('participant/<int:pk>/edit/',
         views.participant_update, name='participant-update'),
    path('participant/<int:pk>/delete/',
         views.participant_delete, name='participant-delete'),


]
