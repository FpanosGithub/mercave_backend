# Generated by Django 4.0.4 on 2022-05-20 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Linea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=16, unique=True)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PuntoRed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=16, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
                ('pkilometrico', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(default=-3.982)),
                ('lat', models.FloatField(default=40.2951)),
                ('linea', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='red_ferroviaria.linea')),
            ],
        ),
    ]