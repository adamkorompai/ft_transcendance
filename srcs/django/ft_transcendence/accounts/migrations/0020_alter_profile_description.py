# Generated by Django 4.2.11 on 2024-04-30 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(default='Phoenix Fury: A mystical warrior capable of summoning flames, rising from ashes to conquer.'),
        ),
    ]
