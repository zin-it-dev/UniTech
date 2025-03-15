from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static

from configs.settings import base

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apis.urls")),
    path("o/", include(oauth2_urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# if base.DEBUG:
#     urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
