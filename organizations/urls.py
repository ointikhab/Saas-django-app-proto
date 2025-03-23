from django.urls import path
from .views import CreateOrganizationView
from .views import ViewOrganizationDetailsView
from .views import RemoveUserFromOrganization
from .views import ChangeSubscriptionView

urlpatterns = [
    path('create/', CreateOrganizationView.as_view(), name='create-organization'),
    path('details/<int:organization_id>/', ViewOrganizationDetailsView.as_view(), name='organization-details'),
    path('remove-user/<int:organization_id>/<int:user_id>/', RemoveUserFromOrganization.as_view(), name='remove-user'),
    path('change-subscription-plan/<int:organization_id>/', ChangeSubscriptionView.as_view(), name='change-subscription'),
]
