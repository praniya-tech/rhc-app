"""project URL Configuration

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
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from rest_framework import routers

from appapi import views as appapi_views


# https://django-allauth.readthedocs.io/en/latest/advanced.html#admin
admin.site.login = login_required(admin.site.login)

appapi_router = routers.DefaultRouter()  # appapi
appapi_router.register(
    prefix=r'svasthyaquestiontype',
    basename='svasthyaquestiontype',
    viewset=appapi_views.SvasthyaQuestionTypeViewSet)
appapi_router.register(
    prefix=r'svasthyaquestionnaire',
    basename='svasthyaquestionnaire',
    viewset=appapi_views.SvasthyaQuestionnaireViewSet)
appapi_router.register(
    prefix=r'prakritipropertytype',
    basename='prakritipropertytype',
    viewset=appapi_views.PrakritiPropertyTypeViewSet)
appapi_router.register(
    prefix=r'prakritioptiontype',
    basename='prakritioptiontype',
    viewset=appapi_views.PrakritiOptionTypeViewSet)
appapi_router.register(
    prefix=r'prakritiquestionnaire',
    basename='prakritiquestionnaire',
    viewset=appapi_views.PrakritiQuestionnaireViewSet)


urlpatterns = [
    path('', include('webapp.urls')),

    # https://django-allauth.readthedocs.io/en/latest/installation.html
    path('accounts/', include('allauth.urls')),

    path('admin/', admin.site.urls),
    # https://github.com/d-demirci/django-adminlte3/issues/33
    path("logout/", lambda request: redirect("/admin/logout", permanent=False)),

    path('appapi/', include(appapi_router.urls)),
    path('appapi-auth/', include('rest_framework.urls')),
]
