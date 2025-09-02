# support_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from resources import views as resource_views
from django.conf import settings
from django.conf.urls.static import static

# The router provides an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'links', resource_views.ResourceLinkViewSet, basename='resourcelink')
router.register(r'sets', resource_views.ResourceSetViewSet, basename='resourceset')

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/qr/<int:pk>/', resource_views.generate_qr_code, name='link-qrcode'),
    path('markdownx/', include('markdownx.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# This is helpful for serving media files during local development,
# though in production they are served from Firebase Storage.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)