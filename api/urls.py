from django.urls import path, include, re_path
from allauth.account import views
from rest_auth.views import LoginView, UserDetailsView
from rest_auth.registration.views import RegisterView
from targets.views import TopicViewSet, TargetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('topics', TopicViewSet, basename='topic')
router.register('targets', TargetViewSet, basename='target')

urlpatterns = [
    path('', include(router.urls)),
    path('account/', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(), name='account_email_verification_sent'),
    re_path('registration/account-confirm-email/<str:key>/login/', LoginView.as_view(), name='login_after_confirm'),
    re_path('registration/account-confirm-email/<str:key>/', views.ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('registration/', include('rest_auth.registration.urls')),
    path('', include('rest_auth.urls')),
]
