# Generated by Django 5.0.6 on 2024-05-30 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rastrobotDjango', '0002_remove_esp32data_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='esp32data',
            old_name='key1',
            new_name='sensorDireito',
        ),
        migrations.RenameField(
            model_name='esp32data',
            old_name='key2',
            new_name='sensorEsquerdo',
        ),
    ]
