from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, UserSerializer

User = get_user_model()


# 회원가입 (POST /api/v1/accounts/signup/)
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]  # 누구나 회원가입 가능


# 로그인 (POST /api/v1/accounts/login/)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """이메일과 비밀번호를 받아 JWT 토큰 발급"""
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "이메일 또는 비밀번호가 올바르지 않습니다."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# 로그아웃 (POST /api/v1/accounts/logout/)
class LogoutView(APIView):

    def post(self, request):
        """리프레시 토큰을 블랙리스트에 추가하여 로그아웃 처리"""
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()  # 토큰 블랙리스트에 추가 (token_blacklist 활성화 필요)
            return Response(
                {"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "유효하지 않은 토큰입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
