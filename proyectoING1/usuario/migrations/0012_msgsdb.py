# Generated by Django 4.2.11 on 2024-05-01 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0011_remove_postsdb_fecha_postsdb_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='MsgsDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.CharField(max_length=40)),
                ('correof', models.CharField(max_length=40)),
                ('msg', models.CharField(max_length=100)),
                ('hora', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
