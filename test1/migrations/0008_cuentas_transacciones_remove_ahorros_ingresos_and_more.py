# Generated by Django 4.2.4 on 2023-08-14 18:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0007_alter_usuario_email_alter_usuario_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuentas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('saldo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transacciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.datetime(2023, 8, 14, 13, 29, 31, 125276))),
                ('monto', models.IntegerField()),
                ('fuente', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='ahorros',
            name='ingresos',
        ),
        migrations.DeleteModel(
            name='Gastos',
        ),
        migrations.DeleteModel(
            name='Ahorros',
        ),
        migrations.DeleteModel(
            name='Ingresos',
        ),
    ]
