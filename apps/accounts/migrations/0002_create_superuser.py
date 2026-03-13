from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_superuser(apps, schema_editor):
    CustomUser = apps.get_model('accounts', 'CustomUser')

    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create(
            username='admin',
            email='admin@example.com',
            password=make_password('Admin@123'),
            is_staff=True,
            is_superuser=True,
            is_active=True,
            role='employer',
        )


def remove_superuser(apps, schema_editor):
    CustomUser = apps.get_model('accounts', 'CustomUser')
    CustomUser.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser, remove_superuser),
    ]