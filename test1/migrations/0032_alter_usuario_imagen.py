# Generated by Django 4.2.4 on 2023-09-13 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0031_alter_usuario_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='imagen',
            field=models.ImageField(blank=True, default='images/icon-user.png', null=True, upload_to='images'),
        ),
    ]