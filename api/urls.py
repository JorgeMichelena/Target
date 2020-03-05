from django.urls import path, include, re_path
from allauth.account import views
from rest_auth.views import LoginView, UserDetailsView
from rest_auth.registration.views import RegisterView
from targets.views import TopicsList, CreateTarget, SeeMyTargets

urlpatterns = [
    path('my-targets/', SeeMyTargets.as_view(), name='my_targets'),
    path('create-target/', CreateTarget.as_view(), name='create_target'),
    path('topics/', TopicsList.as_view(), name='topics'),
    path('login/', LoginView.as_view(), name='account_email_verification_sent'),
    re_path(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/login/$', LoginView.as_view(), name='login_after_confirm'),
    re_path(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', views.ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('registration/', include('rest_auth.registration.urls')),
    path('', include('rest_auth.urls')),
]
