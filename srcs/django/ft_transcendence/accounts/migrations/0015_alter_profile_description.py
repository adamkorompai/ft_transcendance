# Generated by Django 4.2.11 on 2024-04-30 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_remove_profile_losses_remove_profile_wins_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(default="Serpent's Wrath: A nimble warrior skilled in dual-wielding blades, striking with venomous speed."),
        ),
    ]