"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, reverse_lazy
from django.urls.conf import include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.views.generic.base import RedirectView

_DJANGO_URL_PATTERNS = [
    path('admin/', admin.site.urls),
]

_THIRD_PARTY_URL_PATTERNS = [
    # Django Oauth Toolkit
    path('auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # Rosetta
    path('rosetta/', include('rosetta.urls')),
    # DRF Spectacular
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'schema/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger',
    ),
    path(
        'schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]

_MY_URL_PATTERNS = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('', include('services.users.urls')),
    path('', include('services.account_recovery.urls')),
]

urlpatterns = _DJANGO_URL_PATTERNS + _THIRD_PARTY_URL_PATTERNS + _MY_URL_PATTERNS
