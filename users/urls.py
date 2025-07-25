from django.urls import path
from users.views import (
    RegistrationAPIView, 
    AuthorizationAPIView, 
    ConfirmUserAPIView, 
    SendConfirmationCodeView, 
    VerifyCodeView
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import CustomTokenObtainPairView
from users.oauth import GoogleLoginView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView.as_view()),
    path('confirm/', ConfirmUserAPIView.as_view()),

    path('jwt-token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('google-login/', GoogleLoginView.as_view()),

    path('send-code/', SendConfirmationCodeView.as_view()),
    path('verify-code/', VerifyCodeView.as_view()),
]
