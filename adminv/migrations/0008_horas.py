# Generated by Django 4.2.3 on 2023-07-14 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminv', '0007_materiales_familia_alter_materiales_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('horaEnt', models.TimeField()),
                ('horaSal', models.TimeField()),
                ('ubicacion', models.CharField(blank=True, max_length=100, null=True)),
                ('idUsuario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'app_Horas',
            },
        ),
    ]
