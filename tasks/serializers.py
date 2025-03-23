from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task
from projects.serializers import ProjectSerializer

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'status', 'project']
        extra_kwargs = {'project': {'read_only': True}}



class AssignTaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True
    )
    task_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Task
        fields = ['task_id', 'assigned_users']

    def validate(self, data):
        task_id = data.get('task_id')
        project_id = self.context.get('project_id')

        if not Task.objects.filter(id=task_id, project_id=project_id).exists():
            raise serializers.ValidationError({'task_id': 'Task does not exist in the specified project.'})

        return data


class RetrieveTaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.SerializerMethodField()
    project = ProjectSerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'status', 'project', 'assigned_users']

    def get_assigned_users(self, obj):
        """
        Returns a list of assigned users as a dictionary with id and email.
        """
        return [{'id': user.id, 'email': user.email} for user in obj.assigned_users.all()]

