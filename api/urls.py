from django.urls import path, include, re_path
from allauth.account import views
from rest_auth.views import LoginView, UserDetailsView, PasswordResetConfirmView
from rest_auth.registration.views import RegisterView

urlpatterns = [
    path('account/', include('django.contrib.auth.urls')),
    re_path(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/user/$', LoginView.as_view(), name='user_after_confirm'),
    re_path(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/login/$', LoginView.as_view(), name='login_after_confirm'),
    re_path(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', views.ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('registration/', include('rest_auth.registration.urls')),
    path('', include('rest_auth.urls')),
    path('login/', LoginView.as_view(), name='account_email_verification_sent'),
]
