from django.urls import path
from .views import home_view, admin_dashboard, manage_user, group_list, create_group, user_delete, participant_dashboard

urlpatterns = [
    path('', home_view, name='home'),

    path('dashboard/admin/', admin_dashboard, name='admin-dashboard'),
    path('dashboard/admin/manage-user/<int:user_id>/',
         manage_user, name='manage-user'),
    path('dashboard/admin/groups/', group_list, name='group-list'),
    path('dashboard/admin/groups/create/', create_group, name='create-group'),
    path('<int:pk>/delete/', user_delete, name='user-delete'),
    path('dashboard/participant/', participant_dashboard, name='participant-dashboard'),
]
