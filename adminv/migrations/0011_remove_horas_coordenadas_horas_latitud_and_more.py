# Generated by Django 4.2.3 on 2023-09-01 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminv', '0010_rename_horaent_horas_hora_remove_horas_horasal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horas',
            name='coordenadas',
        ),
        migrations.AddField(
            model_name='horas',
            name='latitud',
            field=models.CharField(default=1, max_length=15),
        ),
        migrations.AddField(
            model_name='horas',
            name='longitud',
            field=models.CharField(default=1, max_length=15),
        ),
    ]
