from django.db import models
from organizations.models import Organization

class Project(models.Model):
    title = models.CharField(max_length=255, db_index=True, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="projects")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title
