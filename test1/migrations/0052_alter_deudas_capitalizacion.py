# Generated by Django 4.2.4 on 2023-10-06 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0051_alter_deudas_descripcion_deuda_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deudas',
            name='capitalizacion',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]
