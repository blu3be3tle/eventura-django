from django.urls import path
from .views import (
    EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView,
    category_list, category_detail, category_create, category_update, category_delete,
    rsvp_event
)

urlpatterns = [

    # Event
    path('list/', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('new/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('<int:pk>/rsvp/', rsvp_event, name='rsvp-event'),

    # Category
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
    path('categories/new/', category_create, name='category-create'),
    path('categories/<int:pk>/edit/', category_update, name='category-update'),
    path('categories/<int:pk>/delete/', category_delete, name='category-delete'),
]
