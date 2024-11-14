from rest_framework.permissions import BasePermission

class IsAdminOrWaiter(BasePermission):
    def has_permission(self, request, view):
        # Ensure user is authenticated and is in the 'admin' or 'waiter' group
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name__in=['admin', 'waiter']).exists() or request.user.is_superuser
        return False