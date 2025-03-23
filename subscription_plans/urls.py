from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet

router = DefaultRouter()

router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscription-plan')

# Include router URLs in urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
