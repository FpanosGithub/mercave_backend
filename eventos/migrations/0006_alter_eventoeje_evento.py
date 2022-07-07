# Generated by Django 4.0.4 on 2022-06-10 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_remove_alarmaaceleracion_ax0_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoeje',
            name='evento',
            field=models.CharField(choices=[('START', 'EMPIEZA'), ('STOP', 'PARA'), ('CIRC', 'CIRCULANDO'), ('NUDO', 'NUDO'), ('ALARM_TEMP', 'ALARMA_TEMPERATURA'), ('ALARM_ACEL', 'ALARMA_ACELERACIONES'), ('ALARM_CAMB', 'ALARMA_CAMBIO'), ('INIT_MANT', 'INICIO_MANTENIMIENTO'), ('FIN_MANT', 'FIN_MANTENIMIENTO'), ('CAMBIO', 'CAMBIO_ANCHO')], default='CIRC', max_length=12),
        ),
    ]