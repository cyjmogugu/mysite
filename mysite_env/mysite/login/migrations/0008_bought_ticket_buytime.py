# Generated by Django 2.2 on 2020-05-22 08:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20200522_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='bought_ticket',
            name='buytime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
