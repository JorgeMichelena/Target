from django.urls import path, include
from allauth.account import views
from rest_auth.views import LoginView
from targets.views import TopicViewSet, TargetViewSet
from chat.views import MatchViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('topics', TopicViewSet, basename='topic')
router.register('targets', TargetViewSet, basename='target')
router.register('matches', MatchViewSet, basename='match')

urlpatterns = [
    path('', include(router.urls)),
    path('account/', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(), name='account_email_verification_sent'),
    path('registration/account-confirm-email/<str:key>/login/',
         LoginView.as_view(),
         name='login_after_confirm'
         ),
    path('registration/account-confirm-email/<str:key>/',
         views.ConfirmEmailView.as_view(),
         name='account_confirm_email'
         ),
    path('registration/', include('rest_auth.registration.urls')),
    path('', include('rest_auth.urls')),
    path('login/', LoginView.as_view(), name='account_email_verification_sent'),
]
