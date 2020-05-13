"""target URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.contrib.gis import admin
from django.urls import path, include
from django.views.generic import TemplateView
from chat.views import onesignal_register
from chat.views import onesignal_unregister


urlpatterns = [
    path('chat/', include('chat.urls')),
    path('api/v1/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('manifest.json',
         TemplateView.as_view(template_name='onesignal/manifest.json',
                              content_type='application/json')
         ),
    path('OneSignalSDKWorker.js',
         TemplateView.as_view(template_name='onesignal/OneSignalSDKWorker.js',
                              content_type='application/x-javascript')
         ),
    path('OneSignalSDKWorker.js',
         TemplateView.as_view(template_name='onesignal/OneSignalSDKWorker.js',
                              content_type='application/x-javascript')
         ),
    path('onesignal-register/', onesignal_register, name='onesignal_register'),
    path('onesignal-unregister/', onesignal_unregister, name='onesignal_unregister'),
]
