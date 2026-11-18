from django.db import migrations


def fill_slugs(apps, schema_editor):
    Car = apps.get_model('cars', 'Car')
    for car in Car.objects.using(schema_editor.connection.alias).all():
        car.slug = f'car-{car.pk}'
        car.save(update_fields=['slug'])


class Migration(migrations.Migration):
    dependencies = [('cars', '0002_slug_nullable')]
    operations = [migrations.RunPython(fill_slugs, migrations.RunPython.noop)]
