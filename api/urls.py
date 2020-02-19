from django.urls import path, include

urlpatterns = [
    path('', include('rest_auth.urls')),
]
