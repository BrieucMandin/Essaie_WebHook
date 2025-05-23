"""
URL configuration for Essaie_Webhook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from Football.views.views_api import JoueurViewSet, EntraineurViewSet, EquipeViewSet

router = DefaultRouter()
router.register(r"joueurs", JoueurViewSet, basename="joueur")
router.register(r"entraineurs", EntraineurViewSet, basename="entraineur")
router.register(r"equipes", EquipeViewSet, basename="equipe")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    # Spectacular Schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Redoc UI
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
