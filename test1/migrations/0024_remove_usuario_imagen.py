# Generated by Django 4.2.4 on 2023-09-08 04:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("test1", "0023_usuario_imagen"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usuario",
            name="imagen",
        ),
    ]
