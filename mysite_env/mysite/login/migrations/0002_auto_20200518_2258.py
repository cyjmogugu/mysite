# Generated by Django 2.2 on 2020-05-18 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_form',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
