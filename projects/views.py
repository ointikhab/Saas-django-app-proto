from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from organizations.models import Organization
from saas.custom_permissions import IsOrganizationMember

from .models import Project
from .serializers import ProjectSerializer


class CreateProjectView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        organization_id = self.kwargs.get("organization_id")

        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            return Response({"detail": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            project_title = serializer.validated_data['title']
            project_description = serializer.validated_data['description']
            project = Project.objects.create(
                title=project_title,
                description=project_description,
                organization=organization,
            )
           
            success_message = {
                "message": f"Project '{project.title}' created for '{organization.name}' successfully",
            }

            return Response(success_message, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    