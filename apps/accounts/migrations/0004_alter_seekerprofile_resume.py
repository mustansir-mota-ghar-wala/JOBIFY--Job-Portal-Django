from django.core.files.storage import FileSystemStorage
from django.db import migrations, models

try:
    import cloudinary_storage.storage
except ImportError:  # pragma: no cover - local fallback when optional dependency is missing
    cloudinary_storage = None


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seekerprofile",
            name="resume",
            field=models.FileField(
                blank=True,
                null=True,
                storage=(
                    cloudinary_storage.storage.RawMediaCloudinaryStorage()
                    if cloudinary_storage
                    else FileSystemStorage()
                ),
                upload_to="resumes/",
            ),
        ),
    ]
