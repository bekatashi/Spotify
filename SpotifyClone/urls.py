from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include, re_path
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Music Streaming Project API",
      default_version='v1',
      description='This is test blog project',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), re_path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('song.urls')),
    path('api/v1/accounts/', include('account.urls')),
    path('api/v1/ratings/', include('rating.urls')),
    path('api/v1/paypel/', include('base.urls'))
]

# urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
