from django.urls import path, include
from . import views


urlpatterns = [
    # Event
    path('', views.event_list, name='event-list'),
    path('event/<int:pk>/', views.event_detail, name='event-detail'),
    path('event/new/', views.event_create, name='event-create'),
    path('event/<int:pk>/edit/', views.event_update, name='event-update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event-delete'),
    path('organizer-dashboard/', views.organizer_dashboard, name='dashboard'),
    path("__reload__/", include("django_browser_reload.urls")),

    # Category
    path('categories/', views.category_list, name='category-list'),
    path('category/<int:pk>/', views.category_detail, name='category-detail'),
    path('category/new/', views.category_create, name='category-create'),
    path('category/<int:pk>/edit/', views.category_update, name='category-update'),
    path('category/<int:pk>/delete/',
         views.category_delete, name='category-delete'),
]
