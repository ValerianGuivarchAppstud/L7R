# Generated by Django 3.0.5 on 2020-05-14 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applsr', '0009_viking_agriculture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viking',
            name='point_de_pouvoir_max',
        ),
    ]
