from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model('jobs', 'Category')

    category_names = [
        'IT',
        'Marketing',
        'Finance',
        'HR',
        'Sales',
        'Design',
    ]

    for name in category_names:
        Category.objects.get_or_create(name=name)


def remove_categories(apps, schema_editor):
    Category = apps.get_model('jobs', 'Category')
    Category.objects.filter(
        name__in=['IT', 'Marketing', 'Finance', 'HR', 'Sales', 'Design']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_savedjob'),
    ]

    operations = [
        migrations.RunPython(create_categories, remove_categories),
    ]