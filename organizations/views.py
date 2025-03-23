from django.db.models import Prefetch

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from saas.custom_permissions import IsOrganizationAdmin
from saas.pagination import PaginationClass

from users.models import UserOrganizationMembership
from subscription_plans.models import SubscriptionPlan

from .models import Organization
from .serializers import (
    OrganizationDetailSerializer,
    OrganizationSerializer,
    ChangeSubscriptionSerializer
)
from .signals import assign_organization_to_user_and_make_him_admin



class CreateOrganizationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = OrganizationSerializer(data=request.data)

        if serializer.is_valid():
            organization = serializer.save()
            assign_organization_to_user_and_make_him_admin(
             Organization,
             organization,
             True,
             user=request.user
            )
            success_message = {
                'message': f'Organization "{organization.name}" created successfully',
            }

            return Response(success_message, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewOrganizationDetailsView(generics.ListAPIView):
    serializer_class = OrganizationDetailSerializer
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    pagination_class = PaginationClass

    def get_queryset(self):
        '''
        Only allow access to the requested organization if the user is an admin.
        '''
        organization_id = self.kwargs.get('organization_id')
        return Organization.objects.filter(id=organization_id).select_related('subscription_plan').prefetch_related(
            Prefetch(
                'userorganizationmembership_set',
                queryset=UserOrganizationMembership.objects.select_related('user'),
                to_attr='memberships'
            )
        )
    

class RemoveUserFromOrganization(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]

    def delete(self, request, *args, **kwargs):
        organization_id = kwargs.get('organization_id')
        user_id_to_be_deleted = kwargs.get('user_id')

        deleted_count, _ = UserOrganizationMembership.objects.filter(
            organization_id=organization_id,
            user_id=user_id_to_be_deleted
        ).delete()

        if deleted_count == 0:
            return Response({'detail': 'User not found in this organization.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'User removed from the organization successfully.'}, status=status.HTTP_200_OK)


class ChangeSubscriptionView(APIView):
    """
    API to upgrade or downgrade an organization's subscription plan.
    """
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]

    def patch(self, request, *args, **kwargs):
        organization_id = self.kwargs.get('organization_id')
        organization = Organization.objects.filter(id=organization_id).first()

        if not organization:
            return Response({'error': 'Organization not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChangeSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_plan_id = serializer.validated_data['subscription_plan_id']
        new_plan = SubscriptionPlan.objects.filter(id=new_plan_id).first()

        if not new_plan:
            return Response({'error': 'Invalid subscription plan.'}, status=status.HTTP_400_BAD_REQUEST)

        current_member_of_organizations = UserOrganizationMembership.objects.filter(organization=organization).count()
        
        if current_member_of_organizations > new_plan.max_users:
            user_difference = current_member_of_organizations - new_plan.max_users
            return Response(
                {
                    "error": (
                        "The current number of users in this plan exceeds the max allowed new plan. "
                        "You will have to remove {} users from your organization."
                    ).format(user_difference)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        # Update organization's subscription plan
        organization.subscription_plan = new_plan
        organization.save()

        return Response(
            {
                'message': f'Organization "{organization.name}" subscription changed to "{new_plan.name}" successfully.'
            },
            status=status.HTTP_200_OK
        )
    
