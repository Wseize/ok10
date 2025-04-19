from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to everyone.
    Write access is granted to the owner or staff users.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write/delete allowed if the user is the owner or is staff
        return request.user and (
            obj.seller.owner == request.user or
            request.user.is_staff or
            request.user.is_superuser
        )


from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_staff


class IsSuperUserOrSelf(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read-only access for everyone (optional)
        if request.method in SAFE_METHODS:
            return True

        # Superuser has full access
        if request.user and request.user.is_superuser:
            return True

        # Allow users to update their own account
        return obj == request.user

