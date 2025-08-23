from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def group(*group_names):
    def check_perms(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) or user.is_superuser:
                return True
        raise PermissionDenied
    return user_passes_test(check_perms, login_url='login')


is_admin = group('Admin')

is_organizer = group('Organizer', 'Admin')
