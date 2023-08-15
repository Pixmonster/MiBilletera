# Generated by Django 4.2.4 on 2023-08-15 18:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0012_alter_transacciones_fecha_alter_transacciones_fuente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_categoria', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='transacciones',
            name='categoria',
        ),
        migrations.AddField(
            model_name='cuentas',
            name='transacciones_fk',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='test1.transacciones'),
        ),
        migrations.AlterField(
            model_name='transacciones',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2023, 8, 15, 13, 54, 27, 823210)),
        ),
        migrations.AddField(
            model_name='transacciones',
            name='fk_categoria',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='test1.categoria'),
        ),
    ]