# Generated by Django 4.2.4 on 2023-08-25 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("test1", "0015_remove_cuentas_tipo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cuentas",
            name="fk_user",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"is_superuser": False},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]