from django.urls import path
from . import views
from .views import signup, signin, signout, activate_user

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', signin, name='login'),
    path('logout/', signout, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate'),
]
