from django.urls import path, include
from . import views
from .views import home_view


urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', views.organizer_dashboard, name='dashboard'),
]
