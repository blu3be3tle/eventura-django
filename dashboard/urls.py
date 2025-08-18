from django.urls import path
from .views import (
    dashboard,
    admin_dashboard,
    manage_user,
    user_delete,
    group_list,
    create_group,
    participant_dashboard,
    organizer_dashboard,
)

urlpatterns = [
    # Shared
    path('dashboard/', dashboard, name='dashboard'),

    # Admin
    path('dashboard/admin/', admin_dashboard, name='admin-dashboard'),
    path('dashboard/admin/users/<int:user_id>/',
         manage_user, name='manage-user'),
    path('dashboard/admin/users/<int:user_id>/delete/',
         user_delete, name='user-delete'),
    path('dashboard/admin/groups/', group_list, name='group-list'),
    path('dashboard/admin/groups/create/', create_group, name='create-group'),

    # Others
    path('dashboard/participant/', participant_dashboard,
         name='participant-dashboard'),
    path('dashboard/organizer/', organizer_dashboard, name='organizer-dashboard'),
]
