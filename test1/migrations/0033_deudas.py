# Generated by Django 4.2.4 on 2023-09-25 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0032_alter_usuario_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deudas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_deuda', models.TextField(max_length=50)),
                ('valor_total_deuda', models.DecimalField(decimal_places=2, max_digits=15)),
                ('tipo_de_interes', models.CharField(max_length=50)),
                ('valor_de_interes_mensual', models.FloatField()),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]