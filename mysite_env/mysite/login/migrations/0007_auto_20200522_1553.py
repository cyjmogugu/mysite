# Generated by Django 2.2 on 2020-05-22 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20200522_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bought_ticket',
            name='idnum',
            field=models.CharField(max_length=100),
        ),
    ]
