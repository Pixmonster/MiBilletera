# Generated by Django 4.2.4 on 2023-08-17 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0006_categoriagasto_fuenteingreso_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuentas',
            name='saldo',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='transacciones',
            name='fk_categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='test1.categoriagasto'),
        ),
        migrations.AlterField(
            model_name='transacciones',
            name='fk_fuente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='test1.fuenteingreso'),
        ),
        migrations.AlterField(
            model_name='transacciones',
            name='monto',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
