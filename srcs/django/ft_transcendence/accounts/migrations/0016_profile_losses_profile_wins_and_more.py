# Generated by Django 4.2.11 on 2024-04-30 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_profile_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='wins',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(default='Phoenix Fury: A mystical warrior capable of summoning flames, rising from ashes to conquer.'),
        ),
    ]
