from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from intellijobs.tasks import send_email_verfication
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.validators import UniqueValidator
from users.abstract import District, Province
from .models import UserProfile

User = get_user_model()
account_activation_token = PasswordResetTokenGenerator()


class UserSerializer(serializers.ModelSerializer):
    """ To register a new user """

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "user_type"]
        extra_kwargs = {
            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="This email is already taken."
                    )
                ]
            },
            'username': {
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="This username is already taken."
                    )
                ]
            }
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        # send email to candidate and organization for email verification
        subject = "Email Verification - Intellijobs"
        message = render_to_string('email-templates/email-verification.html', {
            'logo': request.build_absolute_uri('/static/assets/images/logo.png'),
            'user': user,
            'domain': get_current_site(request),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'url': request.build_absolute_uri('/'),
            'token': PasswordResetTokenGenerator.make_token(self=account_activation_token, user=user),
        })

        send_email_verfication.delay(
            subject, message, validated_data.get('email'))

        return user


class UserGetSerializer(serializers.ModelSerializer):
    """ Serializer to get details of user """
    name = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "name",
                  "email", "user_type", "picture"]

    def get_name(self, obj):
        if obj.user_type == "Candidate":
            return obj.user_profile.get_full_name()
        elif obj.user_type == "Organization":
            return obj.org_profile.name
        else:
            return obj.email

    def get_picture(self, obj):
        request = self.context.get('request')
        if obj.user_type == "Candidate" and obj.user_profile and obj.user_profile.display_picture:
            return request.build_absolute_uri(obj.user_profile.display_picture.url)
        elif obj.user_type == "Organization" and obj.org_profile.display_picture:
            return request.build_absolute_uri(obj.org_profile.display_picture.url)
        else:
            return None


class GetUserProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()
    display_picture = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_name(self, obj):
        return obj.get_full_name()

    def get_email(self, obj):
        return obj.user.email

    def get_dob(self, obj):
        if obj.dob:
            return obj.dob.strftime("%b %d, %Y")
        return None

    def get_display_picture(self, obj):
        request = self.context.get('request')
        if obj.display_picture:
            return request.build_absolute_uri(obj.display_picture.url)
        return None


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class UpdateUserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "province", "district", "area", "city", "description"]

    def validate(self, attrs):
        district = attrs.get('district')
        province = attrs.get('province')
        if district.province != province:
            raise serializers.ValidationError(
                {"message": "Selected Province and District does not match."})
        return super().validate(attrs)


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["id", "first_name", "middle_name", "last_name",
                  "email", "mobile_number", "dob", "gender"]

    def get_email(self, obj):
        return obj.user.email
