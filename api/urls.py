from django.urls import path, include

urlpatterns = [
    path('registration/', include('rest_auth.registration.urls')),
    path('', include('rest_auth.urls')),
]
