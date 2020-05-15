from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from api.serializers import MailSerializer
from rest_framework import status
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class MailAdmins(APIView):
    serializer_class = MailSerializer

    def post(self, request):
        admin_mails = User.objects.values_list('email', flat=True).filter(is_superuser=True)
        data_mail = MailSerializer(data=request.data)
        user = request.user
        if data_mail.is_valid():
            message = data_mail['message'].value
            subject = data_mail['subject'].value
            name = 'Anonymous user'
            email = 'No e-mail'
            if user.is_authenticated:
                name = user.username
                email = user.email
            message = f'From: {name}\nEmail: {email}\n\n {message} \n'
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=admin_mails,
                      )
            return Response('Message sent to admins')
        return Response(data_mail.errors, status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
