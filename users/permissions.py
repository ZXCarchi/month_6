from rest_framework.permissions import BasePermission
from datetime import date

class IsEighteen(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or not user.birthday:
            return False
        today = date.today()
        age = today.year - user.birthday.year - ((today.month, today.day) < (user.birthday.month, user.birthday.day))
        return age >= 18