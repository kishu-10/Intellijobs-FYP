from django.urls.conf import path

from users.views import GetUserDetailsView, VerifyEmail

app_name = "users"

urlpatterns = [
    path('verify-email/<uidb64>/<token>/', VerifyEmail.as_view(), name="verify_email"),
    path('detail-<int:pk>/', GetUserDetailsView.as_view(), name="user_details")
]
