from django.urls import path, include
from . import views


urlpatterns = [
    # User
    path('users/', views.user_list, name='user-list'),
    path('user/<int:pk>/', views.user_detail,
         name='user-detail'),
    path('user/new/', views.user_create, name='user-create'),
    path('user/<int:pk>/edit/',
         views.user_update, name='user-update'),
    path('user/<int:pk>/delete/',
         views.user_delete, name='user-delete'),

]
