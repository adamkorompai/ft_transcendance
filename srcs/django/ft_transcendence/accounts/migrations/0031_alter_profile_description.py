# Generated by Django 4.2.11 on 2024-03-14 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_alter_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(default='Shadow Fang: A cunning assassin, striking swiftly from the darkness with deadly precision.'),
        ),
    ]
