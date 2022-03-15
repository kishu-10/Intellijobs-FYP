from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        try:
            data['username'] = self.user.username
            data['email'] = self.user.email
            data["user_type"] = self.user.user_type
            data["verified_email"] = self.user.is_email_verified
            if self.user.user_type == "Candidate":
                data['name'] = self.user.user_profile.get_full_name()
            else:
                data['name'] = self.user.org_profile.name
        except User.DoesNotExist:
            pass
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
