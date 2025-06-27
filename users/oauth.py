import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({"error": "Code is required"}, status=400)
        
        token_response  = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
                "grant_type": "authorization_code",
            }
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"error": "Invalid code"}, status=400)
        
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo", # попробуйте еще https://www.googleapis.com/oauth2/v3/userinfo
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        print(f"user data {user_info}")

        email = user_info["email"]
        first_name = user_info["name"]


        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
            }
        )

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
    