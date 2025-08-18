from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from dashboard.views import no_permission, home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', home_view, name='home'),
    path('no-permission/', no_permission, name='no-permission')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
