from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allow full access only to admin users.
    Read-only for everyone else.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsAdminOrSuperUser(BasePermission):
    """
    Allows access only to Superadmin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_staff))

class IsSuperUserOnly(BasePermission):
    """
    Allows access only to Superadmin users (is_superuser=True).
    is_staff users are NOT allowed unless they are also is_superuser.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)