from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('cars', '0001_initial')]
    operations = [migrations.AddField(
        model_name='car', name='slug',
        field=models.SlugField(max_length=220, null=True, blank=True))]
