from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from users.models import UserProfile
from .serializers import *

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

            return Response({"message": "Email Verified Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid Token. Please enter valid token"}, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()

            # create trainer profile for the instance user
            profile = UserProfile.objects.create(user=user_obj)
            profile.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserDetailsView(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('pk'))
        serializer = UserGetSerializer(user, context={'request': self.request})
        return Response(serializer.data)
