from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView
from .views import  DeleteUserView
from .views import LoginView
from .views import InviteUserToOrganizationView
from .views import AcceptOrRejectInvitation

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete-user'),
    path('invite-user/<int:organization_id>/', InviteUserToOrganizationView.as_view(), name='organization-invitation'),
    path('invitaton-respond/<int:organization_id>/', AcceptOrRejectInvitation.as_view(), name='response-invitation'),
]
