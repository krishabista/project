# Generated by Django 3.1.1 on 2020-09-14 13:03

import agents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='image',
            field=models.ImageField(null=True, upload_to=agents.models.upload_location),
        ),
    ]
