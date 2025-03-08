"""
URL configuration for auto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from baton.autodiscover import admin
from django.conf import settings
from django.apps import apps
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    path('swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('froala/', include('froala.urls')),
    path('admin/defender/', include('defender.urls')),
    path("admin/lookups/", include(ajax_select_urls)),
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('categories/', include('categories.urls')),
    path('tags/', include('tags.urls')),
    path('common/', include('common.urls', namespace='_common')),
    path('blogs/', include('blogs.urls', namespace='blogs')),
    path('common/', include("common.urls")),

    path('rapidoc/', TemplateView.as_view(template_name="common/rapidoc.html"), name="rapidoc")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
