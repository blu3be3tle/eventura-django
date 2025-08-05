from django.urls import path, include
from . import views


urlpatterns = [
    # Participant
    path('participants/', views.participant_list, name='participant-list'),
    path('participant/<int:pk>/', views.participant_detail,
         name='participant-detail'),
    path('participant/new/', views.participant_create, name='participant-create'),
    path('participant/<int:pk>/edit/',
         views.participant_update, name='participant-update'),
    path('participant/<int:pk>/delete/',
         views.participant_delete, name='participant-delete'),

]
