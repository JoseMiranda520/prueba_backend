# Generated by Django 2.1.2 on 2019-01-31 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190123_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz_result',
            name='schedule',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
