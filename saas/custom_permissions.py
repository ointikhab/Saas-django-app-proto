from rest_framework import permissions
from users.models import UserOrganizationMembership
from projects.models import Project

class IsOrganizationAdmin(permissions.BasePermission):
    """
    Custom permission to allow only admin users to access organization details.
    """

    def has_permission(self, request, view):
        
        organization_id = view.kwargs.get('organization_id')

        if not organization_id:
            self.message = "Missing organization id in request."
            return False

        if not UserOrganizationMembership.objects.filter(
            user=request.user, 
            organization_id=organization_id, 
            role='admin'
        ).exists():
            self.message = "This action can only be performed by organization admins."
            return False
            
        return True
    

class IsOrganizationMember(permissions.BasePermission):
    """
    Custom permission to allow only organization member users
    """

    def has_permission(self, request, view):
        
        organization_id = view.kwargs.get('organization_id')

        if not organization_id:
            return False

        # Check if the user is a member in the organization
        if not UserOrganizationMembership.objects.filter(user=request.user, organization_id=organization_id).exists():
            self.message = "It Seems like you are not a member of this organization"
            return False
        return True
    

class IsProjectPartOfOrganization(permissions.BasePermission):
    def has_permission(self, request, view):
        
        organization_id = view.kwargs.get('organization_id')
        project_id = view.kwargs.get('project_id')

        if not organization_id or not project_id:
            self.message = "Missing organization or project ID in request."
            return False

        if not Project.objects.filter(id=project_id, organization_id=organization_id).exists():
            self.message = "This project does not belong to the specified organization."
            return False
        return True
