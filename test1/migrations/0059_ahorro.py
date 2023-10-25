# Generated by Django 4.2.5 on 2023-10-25 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0058_alter_deudas_dia_pago'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ahorro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=15)),
                ('fk_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test1.cuentas')),
            ],
        ),
    ]
