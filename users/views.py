from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from organizations.models import Organization
from saas.custom_permissions import IsOrganizationAdmin

from .models import UserOrganizationInvite, UserOrganizationMembership
from .serializers import (
    AcceptRejectSerializer,
    InviteUserSerializer,
    LoginSerializer,
    RegisterSerializer,
)



def get_tokens_for_user(user):
    """Generate JWT tokens for the user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'tokens': get_tokens_for_user(user)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


class InviteUserToOrganizationView(APIView):
    '''
    ideally email functionality should be there for invitation
    but here i am doing it db and api request to show its working
    '''
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]

    def create_or_get_user(self, email, role, og_id):
        user = User.objects.filter(email=email).first()
        '''
         we can have seperate strategy for creating password as well like set it up via email.
         but for now it is like this
        '''
        password_string = f"{email}{role}{og_id}"
        hashed_password = make_password(password_string)
        if not user:
                user = User.objects.create(
                    email=email,
                    username=email,
                    password=hashed_password
                )
        return user
    
    def create_invite_for_users(self, user, organization, role):
        existing_invite = UserOrganizationInvite.objects.filter(user=user, organization=organization).first()
        if existing_invite:
            if existing_invite.is_expired:
                existing_invite.delete()
            else:
                return Response({
                    'detail': 'User is already invited to this organization and the invitation is still valid till {}.'.format(existing_invite.expiry_at)
                }, status=status.HTTP_400_BAD_REQUEST)
        UserOrganizationInvite.objects.create(
            user=user,
            organization=organization,
            role=role,
            expiry_at=now() + timedelta(days=30)
        )
        return Response({
            'message': f"Invite sent to {user.email} for role {role} in {organization.name}."
        }, status=status.HTTP_201_CREATED)

    def get_organization_member_count(self, organization):
        return UserOrganizationMembership.objects.filter(
            organization=organization
        ).count()
    
    
    def post(self, request, *args, **kwargs):
        '''Handle the invitation of a user to an organization.'''
        organization_id = kwargs.get('organization_id')
        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            return Response({'detail': 'Organization not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = InviteUserSerializer(data=request.data)

        if serializer.is_valid():
            user_email = serializer.validated_data['user_email']
            role = serializer.validated_data['role']

            total_member_in_organization = self.get_organization_member_count(
                organization
            )
            if total_member_in_organization >= organization.subscription_plan.max_users:
                return Response(
                    {'detail': 'Max users reached for this subscription plan'.format(organization.subscription_plan.max_users)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = self.create_or_get_user(
                user_email,
                role,
                organization_id,
            )

            # Optionally, send an email or notification here
            return self.create_invite_for_users(user, organization, role)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AcceptOrRejectInvitation(APIView):
    '''
    Assuming user has a email link to accept or reject the invitation
    '''
    permission_classes = [IsAuthenticated]

    def check_if_invite_exists_for_the_user(self, user, organization):
        return UserOrganizationInvite.objects.filter(user=user, organization=organization).exists()
    
    def check_if_user_already_exists_inorganization(self, user, organization):
        return UserOrganizationMembership.objects.filter(user=user, organization=organization).exists()
    
    def accept_invitation(self, user, organization):
        total_member_in_organization = self.get_organization_member_count(organization)
        if total_member_in_organization >= organization.subscription_plan.max_users:
            return Response(
                {'detail': 'Max users reached for this subscription plan'.format(organization.subscription_plan.max_users)},
                status=status.HTTP_400_BAD_REQUEST
            )
        invitation = UserOrganizationInvite.objects.filter(user=user, organization=organization).first()
        if self.check_if_user_already_exists_inorganization(user, organization=organization):
            return Response({
                'detail': 'User {} is already part of this organization {}'.format(user.username, organization.name)
            }, status=status.HTTP_400_BAD_REQUEST)
        UserOrganizationMembership.objects.create(
            user=user,
            organization=organization,
            role=invitation.role
        )
        invitation.delete()
        return Response({
            'message': 'user {} is now a member of {}.'.format(user.username, organization.name)
        }, status=status.HTTP_201_CREATED)
    
    def reject_invitation(self, user, organization):
        if self.check_if_user_already_exists_inorganization(user,organization):
            return Response({
                'detail': 'You are already part of this organization. This link is no longer valid'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({
            'message': 'Rejected the invitation. Deleting user from our record'
            }, status=status.HTTP_400_BAD_REQUEST,
        )

    def get_organization_member_count(self, organization):
        return UserOrganizationMembership.objects.filter(
            organization=organization
        ).count()
    
    def post(self, request, *args, **kwargs):
        '''Accept or reject the invitation to organization'''
        organization_id = kwargs.get('organization_id')
        user = request.user
        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            return Response({'detail': 'Organization not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not self.check_if_invite_exists_for_the_user(user, organization):
            return Response({'detail': 'Invite Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AcceptRejectSerializer(data=request.data)

        if serializer.is_valid():
            accept_offer = serializer.validated_data['accept_offer']
            if accept_offer:
                return self.accept_invitation(user, organization)
            
            return self.reject_invitation(user, organization)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)