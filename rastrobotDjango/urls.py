"""
URL configuration for rastrobotDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .views import ESP32DataView, ESP32DataListView, ESP32DataDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/esp32/', ESP32DataView.as_view(), name='esp32_data'),
    path('api/esp32/data/', ESP32DataListView.as_view(), name='esp32_data_list'),
    path('api/esp32/data/delete/', ESP32DataDeleteView.as_view(), name='esp32_data_delete'), 

]
