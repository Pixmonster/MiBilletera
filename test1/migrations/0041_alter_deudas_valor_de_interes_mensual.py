# Generated by Django 4.2.4 on 2023-09-26 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0040_alter_deudas_valor_de_interes_mensual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deudas',
            name='valor_de_interes_mensual',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
