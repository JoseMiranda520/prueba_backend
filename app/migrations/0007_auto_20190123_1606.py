# Generated by Django 2.1.2 on 2019-01-23 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20190123_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='entry',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='schedule',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]