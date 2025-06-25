from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperUser(BasePermission):
    """
    Разрешает действия только суперпользователю.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)