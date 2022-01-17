# from rest_framework import serializers
# from intellijobs.validators import MobileNumberValidator
# from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
# from user.models import *
# from django.utils.translation import ugettext_lazy as _

# class AuthUserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(validators=[UniqueValidator(
#         queryset=AuthUser.objects.all())], required=True)
#     phone_number = serializers.CharField(validators=[MobileNumberValidator(
#     ), UniqueValidator(queryset=AuthUser.objects.all())], required=True)

#     class Meta:
#         model = AuthUser
#         exclude = ['uuid','slug', 'is_email_verified']