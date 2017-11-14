from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve
import debug_toolbar

urlpatterns = [
    url(r'^', include('landings.urls')),
    url(r'^', include('user_auth.urls')),
    url(r'^', include('file_processor.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
        )
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]

    urlpatterns += [
            url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
            url(r'^', include('django.contrib.staticfiles.urls')),
        ]