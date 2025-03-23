from rest_framework import viewsets
from .models import SubscriptionPlan
from .serializers import SubscriptionPlanSerializer
from saas.pagination import PaginationClass
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SubscriptionPlanSerializer
    pagination_class = PaginationClass
    