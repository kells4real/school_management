# Generated by Django 2.2.2 on 2020-05-16 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20200516_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
