# Generated by Django 4.2 on 2024-06-13 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plazos', '0003_plazofijo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidad',
            name='monto',
            field=models.FloatField(default=0),
        ),
    ]
