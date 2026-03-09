from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_jobs'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='jobs'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class SavedJob(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_jobs'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='saved_by_users'
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"