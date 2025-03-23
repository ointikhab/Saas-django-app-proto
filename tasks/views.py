from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from saas.custom_permissions import (
    IsOrganizationMember,
    IsProjectPartOfOrganization
)
from saas.pagination import PaginationClass
from organizations.models import Organization
from projects.models import Project
from users.models import UserOrganizationMembership
from .models import Task
from .serializers import (
    TaskSerializer,
    AssignTaskSerializer,
    RetrieveTaskSerializer
)


'''
taking clickup as a reference where tasks are created first then users are assigned.
first i am creating task, then via seperate api i will be assgning user to the task
'''
class CreateNewTask(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember, IsProjectPartOfOrganization]

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        organization_id = self.kwargs.get('organization_id')
        project_id = self.kwargs.get('project_id')

        project = get_object_or_404(Project, id=project_id, organization_id=organization_id)
        
        if serializer.is_valid():
            task = serializer.save(project=project)

            return Response(
                {'message': f"Task '{task.title}' created successfully in project '{project.title}'"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AssignUserTaskView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember, IsProjectPartOfOrganization]

    def post(self, request, *args, **kwargs):
        organization_id = self.kwargs.get('organization_id')
        project_id = self.kwargs.get('project_id')
        serializer = AssignTaskSerializer(data=request.data, context={'project_id': project_id})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        task_id = serializer.validated_data['task_id']
        assigned_user_ids = serializer.validated_data['assigned_users']

        project = get_object_or_404(Project, id=project_id, organization_id=organization_id)
        task = get_object_or_404(Task, id=task_id, project=project)

        assigned_users = []
        for user_id in assigned_user_ids:
            user = get_object_or_404(User, id=user_id)

            # Ensure user belongs to the same organization
            if not UserOrganizationMembership.objects.filter(user=user, organization_id=organization_id).exists():
                return Response(
                    {'error': f"User with ID {user_id} is not a member of the organization."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            assigned_users.append(user)

        task.assigned_users.add(*assigned_users)

        return Response(
            {'message': f"Users successfully assigned to task '{task.title}'"},
            status=status.HTTP_200_OK
        )


class RetrieveTasksView(generics.ListAPIView):
    serializer_class = RetrieveTaskSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'project', 'due_date']
    ordering_fields = ['due_date', 'created_at']
    pagination_class=PaginationClass

    def get_queryset(self):
        """
        Fetch tasks based on filters.
        """
        organization_id = self.kwargs.get('organization_id')
        project_id = self.request.query_params.get('project_id')
        status = self.request.query_params.get('status')
        due_date = self.request.query_params.get('due_date')

        filters = {'project__organization_id': organization_id}

        if project_id:
            filters['project_id'] = project_id
        if status:
            filters['status'] = status
        if due_date:
            filters['due_date'] = due_date

        return Task.objects.filter(**filters)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({'detail': 'No tasks found.'}, status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    