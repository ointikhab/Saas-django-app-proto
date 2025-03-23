from django.db import models

class SubscriptionPlan(models.Model):
    '''
    if needed we can make seperate table with of features with subscription plan table
    but assuming features changes less often and will be textual
    '''
    name = models.CharField(max_length=255, db_index=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_users = models.PositiveIntegerField() 
    features = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
