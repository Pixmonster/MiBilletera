# Generated by Django 4.2.4 on 2023-09-28 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0045_rename_valor_de_interes_fijo_deudas_tasa_de_interes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deudas',
            name='frecuencia_de_pago',
        ),
    ]