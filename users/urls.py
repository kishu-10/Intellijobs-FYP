from django.urls.conf import path

from users.views import *

app_name = "users"

urlpatterns = [
    path('verify-email/<uidb64>/<token>/', VerifyEmail.as_view(), name="verify_email"),
    path('detail-<int:pk>/', GetUserDetailsView.as_view(), name="user_details"),
    path('profile-<int:pk>/', GetUserProfileDetailsView.as_view(), name="profile_details"),
    path('profile/address/update-<int:pk>/', UpdateUserAddressView.as_view(), name="update_profile_address"),
    path('provinces/', GetProvinceListView.as_view(), name="provinces"),
    path('districts/', GetDistrictListView.as_view(), name="districts"),
    path('profile/update-<int:pk>/', UpdateUserProfileView.as_view(), name="update_profile"),

    path('user-profile/create/', CreateUserProfile.as_view(), name="user_profile_create"),
    path('org-profile/create/', CreateOrganizationProfile.as_view(), name="org_profile_create"),
]
