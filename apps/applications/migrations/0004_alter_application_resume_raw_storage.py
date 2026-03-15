from django.core.files.storage import FileSystemStorage
from django.db import migrations, models

try:
    import cloudinary_storage.storage
except ImportError:  # pragma: no cover - local fallback when optional dependency is missing
    cloudinary_storage = None


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0003_application_updated_at_alter_application_resume"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="resume",
            field=models.FileField(
                storage=(
                    cloudinary_storage.storage.RawMediaCloudinaryStorage()
                    if cloudinary_storage
                    else FileSystemStorage()
                ),
                upload_to="application_resumes/",
            ),
        ),
    ]
