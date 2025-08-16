from django.urls import path
from . import views

urlpatterns = [
    # Event
    path('', views.event_list, name='event-list'),
    path('<int:pk>/', views.event_detail, name='event-detail'),
    path('new/', views.event_create, name='event-create'),
    path('<int:pk>/edit/', views.event_update, name='event-update'),
    path('<int:pk>/delete/', views.event_delete, name='event-delete'),
    path('<int:pk>/rsvp/', views.rsvp_event, name='rsvp-event'),

    # Category
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    path('categories/new/', views.category_create, name='category-create'),
    path('categories/<int:pk>/edit/',
         views.category_update, name='category-update'),
    path('categories/<int:pk>/delete/',
         views.category_delete, name='category-delete'),
]
