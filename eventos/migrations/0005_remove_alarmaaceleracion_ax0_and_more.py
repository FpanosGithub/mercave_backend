# Generated by Django 4.0.4 on 2022-05-29 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0007_rename_alarma_aceleraciones_vagon_alarma_and_more'),
        ('red_ferroviaria', '0002_puntored_nudo'),
        ('eventos', '0004_rename_timestamp_eventoeje_dt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax0',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax1',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax2',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax3',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax4',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax5',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax6',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax7',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax8',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ax9',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay0',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay1',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay2',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay3',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay4',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay5',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay6',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay7',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay8',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='ay9',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az0',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az1',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az2',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az3',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az4',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az5',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az6',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az7',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az8',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='az9',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='mensaje',
        ),
        migrations.RemoveField(
            model_name='alarmaaceleracion',
            name='vista',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='mensaje',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t0',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t1',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t2',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t3',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t4',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t5',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t6',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t7',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t8',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='t9',
        ),
        migrations.RemoveField(
            model_name='alarmatemp',
            name='vista',
        ),
        migrations.RemoveField(
            model_name='eventoeje',
            name='alarma_aceleracion',
        ),
        migrations.RemoveField(
            model_name='eventoeje',
            name='alarma_temp',
        ),
        migrations.AddField(
            model_name='alarmaaceleracion',
            name='eje',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='material.eje'),
        ),
        migrations.AddField(
            model_name='alarmatemp',
            name='eje',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='material.eje'),
        ),
        migrations.AlterField(
            model_name='eventoeje',
            name='evento',
            field=models.CharField(choices=[('START', 'EMPIEZA'), ('STOP', 'PARA'), ('CIRC', 'CIRCULANDO'), ('NUDO', 'NUDO'), ('ALARM_TEMP', 'ALARMA_TEMPERATURA'), ('ALARM_ACEL', 'ALARMA_ACELERACIONES'), ('INIT_MANT', 'INICIO_MANTENIMIENTO'), ('FIN_MANT', 'FIN_MANTENIMIENTO'), ('CAMBIO', 'CAMBIO_ANCHO')], default='CIRC', max_length=12),
        ),
        migrations.CreateModel(
            name='EventoVagon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField()),
                ('lng', models.FloatField(default=-3.982)),
                ('lat', models.FloatField(default=40.2951)),
                ('evento', models.CharField(choices=[('START', 'EMPIEZA'), ('STOP', 'PARA'), ('CIRC', 'CIRCULANDO'), ('NUDO', 'NUDO'), ('ALARM_TEMP', 'ALARMA_TEMPERATURA'), ('ALARM_ACEL', 'ALARMA_ACELERACIONES'), ('INIT_MANT', 'INICIO_MANTENIMIENTO'), ('FIN_MANT', 'FIN_MANTENIMIENTO'), ('CAMBIO', 'CAMBIO_ANCHO')], default='CIRC', max_length=12)),
                ('cambio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='eventos.cambio')),
                ('mantenimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='eventos.mantenimiento')),
                ('punto_red', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='red_ferroviaria.puntored')),
                ('vagon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.vagon')),
            ],
        ),
    ]
