from django.db import migrations

def create_staff_group(apps, schema_editor):
    """
    Creates the 'Staff' group and assigns it add, change, and view permissions
    for the main project models, excluding delete permissions.
    """
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Define the models we want to set permissions for
    app_models = {
        'customers': ['customer'],
        'vendors': ['vendor'],
        'vehicles': ['vehicle'],
        'trips': ['trip', 'package', 'rating']
    }

    # Create the 'Staff' group
    staff_group, created = Group.objects.get_or_create(name='Staff')

    for app_label, model_names in app_models.items():
        for model_name in model_names:
            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                permissions = Permission.objects.filter(content_type=content_type)
                for perm in permissions:
                    if not perm.codename.startswith('delete'):
                        staff_group.permissions.add(perm)
            except ContentType.DoesNotExist:
                # This might happen if a model is removed or renamed; safe to ignore in that case
                pass

class Migration(migrations.Migration):

    dependencies = [
         # Make sure this matches your previous migration file
    ]

    operations = [
        migrations.RunPython(create_staff_group),
    ]