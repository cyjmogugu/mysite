# Generated by Django 2.2 on 2020-05-26 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20200525_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='admincode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('check', models.CharField(max_length=100)),
            ],
        ),
    ]