# serializers.py
from rest_framework import serializers
from .models import Organization
from subscription_plans.models import SubscriptionPlan
from subscription_plans.serializers import SubscriptionPlanSerializer
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError


class OrganizationSerializer(serializers.ModelSerializer):
    subscription_plan = serializers.IntegerField(required=True)
    name = serializers.CharField(min_length=2)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'subscription_plan']

    def validate_subscription_plan(self, value):
        if value:
            try:
                subscription_plan = SubscriptionPlan.objects.get(id=value)
            except SubscriptionPlan.DoesNotExist:
                raise NotFound(f"Subscription plan with ID {value} does not exist.")
            return subscription_plan
        return None
    
    def validate_name(self, value):
        if Organization.objects.filter(name=value).exists():
            raise ValidationError(f"An organization with the name '{value}' already exists.")
        return value

    def create(self, validated_data):
        subscription_plan = validated_data.pop('subscription_plan', None)
        organization = Organization.objects.create(**validated_data)

        if subscription_plan:
            organization.subscription_plan = subscription_plan
            organization.save()

        return organization

class OrganizationDetailSerializer(serializers.ModelSerializer):
    subscription_plan = SubscriptionPlanSerializer()
    users = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'subscription_plan', 'users']
    
    def get_users(self, obj):
        return [
            {
                "username": membership.user.username,
                "role": membership.role,
                "email": membership.user.email,
                "id": membership.user.pk,
            }
            for membership in obj.memberships
        ]


class ChangeSubscriptionSerializer(serializers.Serializer):
    subscription_plan_id = serializers.IntegerField()

    def validate_subscription_plan_id(self, value):
        """
        Ensure the subscription plan exists.
        """
        if not SubscriptionPlan.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid subscription plan ID.")
        return value
