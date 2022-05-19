# Generated by Django 4.0.4 on 2022-05-19 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fabricante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('de_ejes', models.BooleanField(default=False)),
                ('de_cambiadores', models.BooleanField(default=False)),
                ('de_bogies', models.BooleanField(default=False)),
                ('de_vagones', models.BooleanField(default=False)),
                ('de_locomotoras', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Organizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=16, unique=True)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('cif', models.CharField(blank=True, max_length=16, null=True)),
                ('logo', models.CharField(blank=True, max_length=150, null=True)),
                ('color_corporativo', models.CharField(blank=True, max_length=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizaciones.organizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Mantenedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('de_ejes', models.BooleanField(default=False)),
                ('de_cambiadores', models.BooleanField(default=False)),
                ('de_bogies', models.BooleanField(default=False)),
                ('de_vagones', models.BooleanField(default=False)),
                ('de_locomotoras', models.BooleanField(default=False)),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizaciones.organizacion')),
            ],
        ),
        migrations.CreateModel(
            name='LicenciaFabricacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=16, unique=True)),
                ('contrato', models.FileField(blank=True, null=True, upload_to='contratos/')),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_final', models.DateField(blank=True, null=True)),
                ('alcance', models.CharField(blank=True, max_length=150, null=True)),
                ('ambito', models.CharField(blank=True, max_length=150, null=True)),
                ('restricciones', models.CharField(blank=True, max_length=150, null=True)),
                ('fabricante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizaciones.fabricante')),
            ],
        ),
        migrations.CreateModel(
            name='Keeper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizaciones.organizacion')),
            ],
        ),
        migrations.AddField(
            model_name='fabricante',
            name='organizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizaciones.organizacion'),
        ),
        migrations.CreateModel(
            name='Diseñador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('de_ejes', models.BooleanField(default=False)),
                ('de_cambiadores', models.BooleanField(default=False)),
                ('de_material_rodante', models.BooleanField(default=False)),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizaciones.organizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Certificador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizaciones.organizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Aprovador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizaciones.organizacion')),
            ],
        ),
    ]