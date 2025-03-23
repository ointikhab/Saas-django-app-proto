from django.urls import path
from .views import CreateNewTask
from .views import AssignUserTaskView
from .views import RetrieveTasksView

urlpatterns = [
    path('create/<int:organization_id>/<int:project_id>', CreateNewTask.as_view(), name='create-task'),
    path('assign-task/<int:organization_id>/<int:project_id>', AssignUserTaskView.as_view(), name='assign-task'),
    path('task-details/<int:organization_id>', RetrieveTasksView.as_view(), name='task-details'),
]
