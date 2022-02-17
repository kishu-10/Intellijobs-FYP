from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from intellijobs.tasks import send_email_verfication
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site


User = get_user_model()
account_activation_token = PasswordResetTokenGenerator()


class UserSerializer(serializers.ModelSerializer):
    """ User Serializer for CRUD """

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        # send email to candidate and organization for email verification
        subject = "Email Verification - Intellijobs"
        message = render_to_string('email_verification.html', {
            'user': user,
            'domain': get_current_site(self.request),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'url': self.request.build_absolute_uri('/'),
            'token': PasswordResetTokenGenerator.make_token(self=account_activation_token, user=user),
        })

        send_email_verfication.delay(
            subject, message, validated_data.get('email'))

        return user

    def update(self, instance, validated_data):
        instance = User.objects.get(pk=validated_data.get('id'))
        instance.update(**validated_data)
        if not instance.check_password(validated_data.get('password')):
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class UserGetSerializer(serializers.ModelSerializer):
    """ Serializer to get details of user """
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name",
                  "email", "password", "user_type"]
