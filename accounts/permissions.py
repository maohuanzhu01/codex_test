from rest_framework.permissions import BasePermission

class IsOrganizationMember(BasePermission):
    """Allows access to users in the 'organization_member' group."""
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.groups.filter(name='organization_member').exists())

class IsOrgAdmin(BasePermission):
    """Allows access to organization admins."""
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (
            user.is_superuser or user.groups.filter(name='organization_admin').exists()
        ))
