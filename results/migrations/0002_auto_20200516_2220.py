# Generated by Django 2.2.2 on 2020-05-16 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
