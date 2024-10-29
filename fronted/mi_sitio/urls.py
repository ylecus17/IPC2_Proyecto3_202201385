"""
URL configuration for mi_sitio project.

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
from django.contrib import admin
from django.urls import path
from proyect3 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cargar/', views.cargar_archivo, name='cargar'),
    path('peticiones/', views.peticiones, name='peticiones'),
    path('ayuda/', views.ayuda, name='ayuda'),
     path('ver_datos/', views.ver_datos, name='ver_datos'),
    path('filtrar_fecha/', views.filtrar_fecha, name='filtrar_fecha'),
    path('filtrar_rango/', views.filtrar_rango, name='filtrar_rango'),
    path('ver_mensajes/', views.ver_mensajes, name='ver_mensajes'),
]
