# Generated by Django 2.2.2 on 2020-08-20 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0015_school_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_admitted',
            field=models.DateField(blank=True, null=True),
        ),
    ]