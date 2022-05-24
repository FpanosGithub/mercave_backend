# Generated by Django 4.0.4 on 2022-05-20 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_remove_puntored_linea_alter_eventoeje_punto_red_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoeje',
            name='evento',
            field=models.CharField(choices=[('START', 'EMPIEZA'), ('STOP', 'PARA'), ('CIRC', 'CIRCULANDO'), ('NUDO', 'NUDO'), ('ALARM_TEMP', 'ALARMA_TEMPERATURA'), ('ALARM_ACEL', 'ALARMA_ACELERACIONES'), ('INIT_MANT', 'INICIO_MANTENIMIENTO'), ('FIN_MANT', 'FIN_MANTENIMIENTO'), ('CAMBIO', 'CAMBIO_ANCHO'), ('BOGIE', 'CAMBIO_BOGIE'), ('VAGON', 'CAMBIO_VAGÓN')], default='CIRC', max_length=12),
        ),
    ]
