from django.db import models
from django.contrib.auth.models import User

from organizations.models import Organization
from django.utils.timezone import now
from django.utils.timezone import timedelta

'''
Assumption: One user belongs to one organization
we can use one to many relation as well if one user belongs to multiple organization
'''
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email
    

class UserOrganizationMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'organization')  # Prevent duplicate user-organization entries

    def __str__(self):
        return f"{self.user.username} - {self.role} at {self.organization.name}"
    

class UserOrganizationInvite(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    expiry_at = models.DateTimeField(default='get_default_expiry')

    @staticmethod
    def get_default_expiry():
        """Returns the default expiry date for the invitation."""
        return now() + timedelta(days=30)
    
    @property
    def is_expired(self):
        """Check if the invitation has expired."""
        return now() > self.expiry_at
    
    def __str__(self):
        return f"{self.user.username} - {self.role} at {self.organization.name} (Expires: {self.expiry_at})"
