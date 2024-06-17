# Generated by Django 4.2 on 2024-06-12 03:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('monto', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Plazo_Fijo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.FloatField(default=0)),
                ('interes', models.FloatField()),
                ('titulo', models.CharField(max_length=100)),
                ('dia', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('num_entidades', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.FloatField()),
                ('fecha', models.DateField()),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plazos.entidad')),
                ('plazo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plazos.plazo_fijo')),
            ],
        ),
        migrations.AddField(
            model_name='entidad',
            name='plazo_fijo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plazos.plazo_fijo'),
        ),
    ]