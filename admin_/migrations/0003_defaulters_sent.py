# Generated by Django 2.2.2 on 2020-05-19 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_', '0002_defaulters'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaulters',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]
