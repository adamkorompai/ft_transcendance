# Generated by Django 4.2.11 on 2024-04-12 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0046_alter_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(default="Serpent's Wrath: A nimble warrior skilled in dual-wielding blades, striking with venomous speed."),
        ),
    ]