from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['username'] = user.username
    refresh['birthday'] = str(user.birthday) if user.birthday else None
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }