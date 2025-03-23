from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assigned_users = models.ManyToManyField(User, related_name='tasks')
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    title = models.CharField(max_length=255, db_index=True, unique=True, default=None, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return f"{self.project.title} - {self.status}"
