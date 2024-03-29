from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("courses.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("order/", include("order.urls")),
    path("instructor/", include("instructor.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
