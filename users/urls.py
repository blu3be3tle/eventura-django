from django.urls import path
from . import views
from .views import signup, signin, signout, activate_user

from .views import (
    ProfileView, EditProfileView, CustomPasswordChangeView
)
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', signin, name='login'),
    path('logout/', signout, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('profile/change-password/',
         CustomPasswordChangeView.as_view(), name='change-password'),
]
