# Generated by Django 4.2.11 on 2024-04-29 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0004_usuariosdb_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmigosDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.CharField(max_length=40)),
                ('correof', models.CharField(max_length=40)),
            ],
        ),
    ]
