from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


User = get_user_model()
account_activation_token = PasswordResetTokenGenerator()

class VerifyEmail(APIView):
    """ To Verify Email of Candidate and Organization """

    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(kwargs.get('uidb64'))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and PasswordResetTokenGenerator.check_token(self=account_activation_token, user=user,
                                                            token=kwargs.get('token')):
            user.is_email_verified = True
            user.save()

            return Response({"message": "Email Verified Successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid Token. Please enter valid token"},status=status.HTTP_400_BAD_REQUEST)
            