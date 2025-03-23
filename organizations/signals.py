from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Organization
from users.models import UserOrganizationMembership

@receiver(post_save, sender=Organization)
def assign_organization_to_user_and_make_him_admin(sender, instance, created, **kwargs):
    """
    Assigns the user who created the organization as the admin.
    """
    user = kwargs.get('user')
    if created and user:
        try:
            user_organization = UserOrganizationMembership.objects.create(
                user=user,
                organization=instance,
                role='admin'
            )
        except Exception:
            # log the exception here
            pass
