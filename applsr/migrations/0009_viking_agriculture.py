# Generated by Django 3.0.5 on 2020-05-12 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applsr', '0008_auto_20200512_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='viking',
            name='agriculture',
            field=models.IntegerField(default=2),
        ),
    ]