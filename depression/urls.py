"""
URL configuration for AquaConnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from depApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login',views.login),
    path('paReg',views.paReg),
    path('coReg',views.coReg),

    path('AdminHome',views.AdminHome),
    path('adminPa',views.adminPa),
    path('adminUpdateUsers',views.adminUpdateUsers),
    path('adminCo',views.adminCo),
    path('adminTests',views.adminTests),
    path('adminUpdatetestStatus',views.adminUpdatetestStatus),


    path('coHome',views.coHome),
    path('coConsultations',views.coConsultations),
    path('coChat',views.coChat),
    path('coReqStatus',views.coReqStatus),
    path('coReport',views.coReport),
    path('coDeleteReport',views.coDeleteReport),


    path('paHome',views.paHome),
    path('paTests',views.paTests),
    path('paAttendTest',views.paAttendTest),
    path('paResults',views.paResults),
    path('paConsultCo',views.paConsultCo),
    path('paRequestCo',views.paRequestCo),
    path('paCounsultation',views.paCounsultation),
    path('paChat',views.paChat),
    path('paReports',views.paReports),


]
