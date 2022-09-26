# Generated by Django 2.1.2 on 2019-02-08 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20190208_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publish',
            name='image',
        ),
        migrations.AddField(
            model_name='publish',
            name='media',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.Media'),
        ),
    ]
