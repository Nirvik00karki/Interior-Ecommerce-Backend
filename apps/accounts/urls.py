from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (EmailTokenObtainPairView, RegisterView, GoogleAuthView, VerifyEmailView, ResendVerificationEmailView
                    , PasswordResetRequestView, PasswordResetValidateView, PasswordResetCompleteView, ShippingAddressViewSet
                    , ShippingZoneViewSet, AdminUserCreateView, UserProfileView)

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", EmailTokenObtainPairView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("admin/users/create/", AdminUserCreateView.as_view(), name="admin-create-user"),
    path("google/", GoogleAuthView.as_view(), name="google_auth"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendVerificationEmailView.as_view(), name="resend-verification"),
    path("password-reset/request/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/validate/", PasswordResetValidateView.as_view(), name="password_reset_validate"),
    path("password-reset/complete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("shipping-addresses/", ShippingAddressViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update'}), name="shipping_addresses"),
    path("shipping-addresses/<int:pk>/", ShippingAddressViewSet.as_view({'delete': 'destroy'}), name="shipping_address_detail"),
    path("shipping-cost/", ShippingZoneViewSet.as_view({'get': 'user_shipping_cost'}), name="shipping_cost"),
]