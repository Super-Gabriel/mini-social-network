# Generated by Django 4.2.11 on 2024-04-27 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_usuariosdb_ison'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariosdb',
            name='ip',
            field=models.CharField(default='', max_length=20),
        ),
    ]
