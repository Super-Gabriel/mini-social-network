# Generated by Django 4.2.11 on 2024-04-25 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsuariosDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('correo', models.CharField(max_length=40)),
                ('contra', models.CharField(max_length=40)),
                ('genero', models.CharField(max_length=1)),
            ],
        ),
    ]
