# Generated by Django 4.2.4 on 2023-10-05 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0048_rename_tasa_de_interes_deudas_tasa_de_interes_anual_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deudas',
            name='valor_interes_anual',
        ),
        migrations.AddField(
            model_name='deudas',
            name='Capitalizacion',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
