from django.urls import path, include
from . import views


urlpatterns = [

    path('organizer-dashboard/', views.organizer_dashboard, name='dashboard'),
    path("__reload__/", include("django_browser_reload.urls")),
]
