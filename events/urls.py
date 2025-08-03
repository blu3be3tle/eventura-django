from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.event_list, name='event-list'),
    path('event/<int:pk>/', views.event_detail, name='event-detail'),
    path('event/new/', views.event_create, name='event-create'),
    path('event/<int:pk>/edit/', views.event_update, name='event-update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event-delete'),
    path('organizer-dashboard/', views.dashboard, name='dashboard'),
    path("__reload__/", include("django_browser_reload.urls"))
]