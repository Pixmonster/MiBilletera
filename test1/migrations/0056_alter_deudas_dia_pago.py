# Generated by Django 4.2.4 on 2023-10-06 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0055_deudas_dia_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deudas',
            name='dia_pago',
            field=models.IntegerField(blank=True, max_length=2, null=True),
        ),
    ]
