# Generated by Django 4.0.4 on 2022-07-07 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0008_eje_ultimo_mant'),
    ]

    operations = [
        migrations.AddField(
            model_name='eje',
            name='alarma_cambio',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
