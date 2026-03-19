from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings
from apps.jobs.models import Job

try:
    import cloudinary_storage.storage
except ImportError:  # pragma: no cover - local fallback when optional dependency is missing
    cloudinary_storage = None


USE_CLOUDINARY_RAW_STORAGE = bool(
    cloudinary_storage
    and settings.CLOUDINARY_STORAGE.get('CLOUD_NAME')
    and settings.CLOUDINARY_STORAGE.get('API_KEY')
    and settings.CLOUDINARY_STORAGE.get('API_SECRET')
)


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(
        storage=(
            cloudinary_storage.storage.RawMediaCloudinaryStorage()
            if USE_CLOUDINARY_RAW_STORAGE
            else FileSystemStorage()
        ),
        upload_to='application_resumes/',
        blank=False,
        null=False
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
