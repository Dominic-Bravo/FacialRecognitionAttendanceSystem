from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.http import Http404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import requests

from .serializers import (
    EmailVerificationSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    OAuthLoginSerializer,
    ResetPasswordSerializer,
    SignupSerializer,
)
from .tasks import send_auth_email_task

User = get_user_model()


def _jwt_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def _decode_uid(uid):
    try:
        return force_str(urlsafe_base64_decode(uid))
    except Exception as exc:
        raise Http404 from exc


def _queue_or_send_email(subject, message, recipient_email):
    try:
        send_auth_email_task.delay(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_email)
    except Exception:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=SignupSerializer,
        responses={201: OpenApiResponse(description="Signup successful. Verification email sent.")},
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = f"{settings.FRONTEND_BASE_URL}/verify-email?uid={uid}&token={token}"
        _queue_or_send_email(
            subject="Verify your email",
            message=f"Use this link to verify your email: {verification_link}",
            recipient_email=user.email,
        )
        return Response(
            {"detail": "Signup successful. Check your email for verification link."},
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiResponse(description="JWT access and refresh tokens returned.")},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.email_verified:
            return Response({"detail": "Please verify your email first."}, status=status.HTTP_403_FORBIDDEN)
        return Response(_jwt_for_user(user), status=status.HTTP_200_OK)


class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=EmailVerificationSerializer,
        responses={200: OpenApiResponse(description="Email verified successfully.")},
    )
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = _decode_uid(serializer.validated_data["uid"])
        user = User.objects.filter(pk=uid).first()
        if not user:
            raise Http404
        if not default_token_generator.check_token(user, serializer.validated_data["token"]):
            return Response({"detail": "Invalid verification token."}, status=status.HTTP_400_BAD_REQUEST)
        user.email_verified = True
        user.save(update_fields=["email_verified"])
        return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: OpenApiResponse(description="Password reset email sent (if account exists).")},
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.FRONTEND_BASE_URL}/reset-password?uid={uid}&token={token}"
            _queue_or_send_email(
                subject="Reset your password",
                message=f"Use this link to reset your password: {reset_link}",
                recipient_email=user.email,
            )
        return Response(
            {"detail": "If the email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: OpenApiResponse(description="Password reset successful.")},
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = _decode_uid(serializer.validated_data["uid"])
        user = User.objects.filter(pk=uid).first()
        if not user:
            raise Http404
        if not default_token_generator.check_token(user, serializer.validated_data["token"]):
            return Response({"detail": "Invalid reset token."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: OpenApiResponse(description="Current authenticated user profile.")},
    )
    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "email": request.user.email,
                "username": request.user.username,
                "role": request.user.role,
                "email_verified": request.user.email_verified,
            }
        )


class OAuthLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=OAuthLoginSerializer,
        responses={200: OpenApiResponse(description="JWT tokens returned from OAuth login.")},
        examples=[
            OpenApiExample(
                "OAuth Login Example",
                value={"provider": "google", "access_token": "provider-access-token"},
                request_only=True,
            )
        ],
    )
    def post(self, request):
        provider = request.data.get("provider")
        access_token = request.data.get("access_token")
        if not provider or not access_token:
            return Response(
                {"detail": "provider and access_token are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        provider = provider.lower()
        profile = self._fetch_profile(provider, access_token)
        if not profile.get("email"):
            return Response({"detail": "Provider email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            email=profile["email"],
            defaults={
                "username": profile.get("username", profile["email"].split("@")[0]),
                "email_verified": True,
            },
        )
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])
        return Response(_jwt_for_user(user), status=status.HTTP_200_OK)

    def _fetch_profile(self, provider, access_token):
        if provider == "google":
            resp = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            )
            data = resp.json()
            return {"email": data.get("email"), "username": data.get("name")}
        if provider == "facebook":
            resp = requests.get(
                "https://graph.facebook.com/me",
                params={"fields": "id,name,email", "access_token": access_token},
                timeout=10,
            )
            data = resp.json()
            return {"email": data.get("email"), "username": data.get("name")}
        if provider == "github":
            headers = {"Authorization": f"Bearer {access_token}"}
            profile_resp = requests.get("https://api.github.com/user", headers=headers, timeout=10).json()
            email_resp = requests.get("https://api.github.com/user/emails", headers=headers, timeout=10).json()
            primary = next((e["email"] for e in email_resp if e.get("primary")), None)
            return {"email": primary, "username": profile_resp.get("login")}
        raise Http404

# Create your views here.
