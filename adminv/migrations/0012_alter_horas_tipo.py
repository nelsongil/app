# Generated by Django 4.2.3 on 2023-09-21 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminv', '0011_remove_horas_coordenadas_horas_latitud_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horas',
            name='tipo',
            field=models.CharField(max_length=3),
        ),
    ]
