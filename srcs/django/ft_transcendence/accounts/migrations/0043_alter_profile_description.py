# Generated by Django 4.2.11 on 2024-03-28 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0042_alter_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(default='Shadow Fang: A cunning assassin, striking swiftly from the darkness with deadly precision.'),
        ),
    ]