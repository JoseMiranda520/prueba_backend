# Generated by Django 2.1.2 on 2019-01-23 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_sale_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
    ]
