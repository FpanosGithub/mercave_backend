# Generated by Django 4.0.4 on 2022-05-27 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_alter_eventoeje_evento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventoeje',
            old_name='timestamp',
            new_name='dt',
        ),
    ]