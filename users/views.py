from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from users.models import CustomUser
from users.utils import get_confirmation_code, save_confirmation_code
from .serializers import (
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer
)
from .models import ConfirmationCode
import random
import string
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer
from .permissions import IsEighteen


class SomePrivateAPIView(APIView):
    permission_classes = [IsEighteen]

    def get(self, request):
        return Response(
            status=status.HTTP_200_OK,
            data={'message': 'You are allowed to see this!'}
        )

class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer
    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User account is not activated yet!'}
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'User credentials are wrong!'}
        )


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        username = serializer.validated_data.get("username")
        password = serializer.validated_data['password']

        # Use transaction to ensure data consistency
        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                password=password,
                is_active=False
            )

            # Create a random 6-digit code
            code = ''.join(random.choices(string.digits, k=6))

            confirmation_code = ConfirmationCode.objects.create(
                user=user,
                code=code
            )
            from users.tasks import send_otp_email
            send_otp_email.delay(email, code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'confirmation_code': code
            }
        )

class ConfirmUserAPIView(APIView):
    @swagger_auto_schema(
            request_body=ConfirmationSerializer
    )
    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            ConfirmationCode.objects.filter(user=user).delete()

        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'User аккаунт успешно активирован',
                'key': token.key
            }
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SendConfirmationCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email обязателен'}, status=400)

        code = str(random.randint(100000, 999999))
        save_confirmation_code(email, code)

        # тут отправка на почту (имитация)
        print(f"Код подтверждения для {email}: {code}")

        return Response({'message': 'Код отправлен'})
    

class VerifyCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({'error': 'Email и код обязательны'}, status=400)

        real_code = get_confirmation_code(email)
        if real_code == code:
            return Response({'message': 'Код подтвержден'})
        else:
            return Response({'error': 'Неверный код'}, status=400)