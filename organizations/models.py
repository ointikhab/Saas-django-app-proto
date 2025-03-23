from django.db import models
from subscription_plans.models import SubscriptionPlan

class Organization(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

