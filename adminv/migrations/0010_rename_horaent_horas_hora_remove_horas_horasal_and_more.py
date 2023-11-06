# Generated by Django 4.2.3 on 2023-07-14 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminv', '0009_alter_horas_horasal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='horas',
            old_name='horaEnt',
            new_name='hora',
        ),
        migrations.RemoveField(
            model_name='horas',
            name='horaSal',
        ),
        migrations.RemoveField(
            model_name='horas',
            name='ubicacion',
        ),
        migrations.AddField(
            model_name='horas',
            name='coordenadas',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='horas',
            name='tipo',
            field=models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
