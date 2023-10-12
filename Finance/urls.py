
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'assistant'


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('test1.urls')),
    path("", include('assistant.urls')),
    path("accounts/", include('django.contrib.auth.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
