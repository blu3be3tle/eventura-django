from django.urls import path
from . import views
from .views import signup, signin, signout

urlpatterns = [
    # User
    path('', views.user_list, name='user-list'),
    path('<int:pk>/', views.user_detail, name='user-detail'),
    # path('new/', views.user_create, name='user-create'),
    # path('<int:pk>/edit/', views.user_update, name='user-update'),
    path('<int:pk>/delete/', views.user_delete, name='user-delete'),

    path('signup/', signup, name='signup'),
    path('login/', signin, name='login'),
    path('logout/', signout, name='logout'),  # type: ignore
]
