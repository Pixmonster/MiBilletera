# Generated by Django 4.2.4 on 2023-10-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0046_remove_deudas_frecuencia_de_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='deudas',
            name='valor_interes',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]