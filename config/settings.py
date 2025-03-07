"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.19.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 환경 변수 로드
env = environ.Env(DEBUG=(bool, False))  # DEBUG 값을 boolean으로 변환, 기본값 False

# .env 파일 로드
environ.Env.read_env(BASE_DIR / ".env")

# ChromaDB 저장 경로 설정
CHROMA_DB_DIR = env("CHROMA_DB_DIR", default=str(BASE_DIR / "chroma_db"))

# API 키 설정
GOV24_API_KEY = env("GOV24_API_KEY")
YOUTH_POLICY_API_KEY = env("YOUTH_POLICY_API_KEY")
EMPLOYMENT_API_KEY = env("EMPLOYMENT_API_KEY")

# PDF 저장 폴더 설정
PDF_DIR = BASE_DIR / "data" / "pdf"

# .env에서 파일명을 불러와서 data/pdf/ 내에서 찾도록 설정
PDF_FILENAME = env("PDF_PATH", default="")
PDF_PATH = str(PDF_DIR / PDF_FILENAME) if PDF_FILENAME else None

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = (
    ["localhost", "127.0.0.1"] if DEBUG else env.list("ALLOWED_HOSTS", default=[])
)


CORS_ALLOWED_ORIGINS = (
    # 프론트엔드가 실행되는 주소 (라이브 서버 플러그인 사용 시)
    ["http://localhost:5500", "http://127.0.0.1:5500"]
    if DEBUG
    else env.list("CORS_ALLOWED_ORIGINS", default=[])
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # 로그아웃 시 토큰 블랙리스트 사용
    "corsheaders",
    "allauth",
    "allauth.account",  # 이메일 로그인 지원
    "allauth.socialaccount",  # 소셜 로그인 지원
    "allauth.socialaccount.providers.google",  # Google 소셜 로그인 지원
    "allauth.socialaccount.providers.kakao",  # 카카오 소셜 로그인 추가
    # Local apps
    "accounts",
    "chatbot",
]


SITE_ID = 1


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # corsheaders 미들웨어 추가
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # django-allauth의 AccountMiddleware
    "allauth.account.middleware.AccountMiddleware",
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # 기본 Django 인증
    "allauth.account.auth_backends.AuthenticationBackend",  # 소셜 로그인 인증
]


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}


# 기본 로그인 필드 설정 (이메일 기반 로그인)
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"  # 이메일 인증
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
SOCIALACCOUNT_ADAPTER = "allauth.socialaccount.adapter.DefaultSocialAccountAdapter"


# allauth 설정 추가
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # username 필드 없음



# 환경에 따라 Google, kakao OAuth 설정 다르게 적용
if DEBUG:  # 개발 환경
    LOGIN_REDIRECT_URL = env("FRONTEND_DEV_URL")
    LOGOUT_REDIRECT_URL = env("FRONTEND_DEV_URL")
else:  # 운영 환경
    LOGIN_REDIRECT_URL = env("FRONTEND_PROD_URL")
    LOGOUT_REDIRECT_URL = env("FRONTEND_PROD_URL")

SOCIALACCOUNT_PROVIDERS = {
    "kakao": {
        "APP": {
            "client_id": env("KAKAO_CLIENT_ID"),  # 카카오 REST API 키
            "secret": env("KAKAO_SECRET"),  # 카카오 Client Secret (필요시)
            "key": "",
        },
        "AUTH_PARAMS": {"prompt": "select_account"},
    },
    "google": {
        "SCOPE": [
            "openid",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APP": {
            "client_id": env("GOOGLE_CLIENT_ID"),
            "secret": env("GOOGLE_CLIENT_SECRET"),
            "redirect_uris": env("GOOGLE_REDIRECT_URI"),
        },
    }
}


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": (
        {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
        if DEBUG
        else env.db("DATABASE_URL")
    )
}


# 사용자 모델 설정
AUTH_USER_MODEL = "accounts.User"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django REST framework settings
REST_FRAMEWORK = {
    # 1. 인증 방식 (JWT + 세션)
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # 일반 API
        "rest_framework.authentication.SessionAuthentication",  # Admin 페이지
    ),
    # 2. 기본 권한 (로그인한 사용자만 API 접근 가능)
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
