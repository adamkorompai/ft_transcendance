# Generated by Django 4.2.11 on 2024-04-12 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0049_alter_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(default='Celestial Guardian: A celestial warrior harnessing divine energy, defending justice with heavenly might.'),
        ),
    ]
