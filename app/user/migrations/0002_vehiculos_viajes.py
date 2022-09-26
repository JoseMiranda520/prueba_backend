# Generated by Django 2.1.2 on 2022-09-25 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculos',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('deleted', models.BooleanField(default=False, verbose_name='Eliminado')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Eliminado el')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizado el')),
                ('active', models.BooleanField(default=True, help_text='Indica si el modelo está operativo', verbose_name='Activo')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cilindraje', models.CharField(max_length=10)),
                ('capacidad', models.CharField(max_length=50)),
                ('placa', models.CharField(max_length=320)),
                ('fecha_soat', models.DateTimeField()),
                ('fecha_tarjeta_operacion', models.DateTimeField()),
                ('estado', models.CharField(choices=[('Disponible', 'Disponible'), ('Ocupado', 'Ocupado'), ('Fuera de servicio', 'Fuera de servicio')], max_length=50)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_vehiculos_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_vehiculos_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propietario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vehiculo',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Viajes',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('deleted', models.BooleanField(default=False, verbose_name='Eliminado')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Eliminado el')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizado el')),
                ('active', models.BooleanField(default=True, help_text='Indica si el modelo está operativo', verbose_name='Activo')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('punto_salida', models.CharField(max_length=50)),
                ('punto_llegada', models.CharField(max_length=50)),
                ('nombre_del_cliente', models.CharField(max_length=50)),
                ('placa_vehiculo', models.CharField(max_length=5, null=True)),
                ('estado', models.CharField(max_length=50)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_viajes_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_viajes_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Viaje',
                'ordering': ['-id'],
            },
        ),
    ]
