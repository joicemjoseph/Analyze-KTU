from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

import debug_toolbar

urlpatterns = [
    url(r'^', include('landings.urls')),
    url(r'^', include('user_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
        )
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]

