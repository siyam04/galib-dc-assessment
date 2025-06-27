from rest_framework.permissions import BasePermission, SAFE_METHODS


# RBAC:
# Public: Anyone (even not logged in) can read public data and register.
# Authenticated: Logged-in users can create and manage their own content and use AI.
# Admin: Only admins can do everything and access certain endpoints (like user list, analytics).


class IsOwnerOrReadOnly(BasePermission):
    """
    - Anyone can read (GET, HEAD, OPTIONS).
    - Only the owner of the object can edit or delete (PUT, PATCH, DELETE).
    - Used on content endpoints so users can only modify their own content.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAdminUser(BasePermission):
    """
    - Only users with is_staff=True (admins) can access the endpoint.
    - Used for user management and analytics endpoints.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
