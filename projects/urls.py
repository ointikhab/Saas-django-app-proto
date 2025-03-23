from django.urls import path
from .views import CreateProjectView

urlpatterns = [
    path('create/<int:organization_id>/', CreateProjectView.as_view(), name='create-project'),
]
