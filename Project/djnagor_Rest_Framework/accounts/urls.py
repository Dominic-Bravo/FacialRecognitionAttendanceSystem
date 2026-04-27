from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ForgotPasswordAPIView,
    LoginAPIView,
    MeAPIView,
    OAuthLoginAPIView,
    ResetPasswordAPIView,
    SignupAPIView,
    VerifyEmailAPIView,
)

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify-email"),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("oauth-login/", OAuthLoginAPIView.as_view(), name="oauth-login"),
    path("me/", MeAPIView.as_view(), name="me"),
]
