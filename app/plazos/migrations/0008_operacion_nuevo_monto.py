# Generated by Django 4.2 on 2024-07-08 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plazos', '0007_alter_operacion_monto'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacion',
            name='nuevo_monto',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
