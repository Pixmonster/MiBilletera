# Generated by Django 4.2.4 on 2023-08-10 15:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("test1", "0005_alter_usuario_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="username",
            field=models.CharField(max_length=60),
        ),
    ]
