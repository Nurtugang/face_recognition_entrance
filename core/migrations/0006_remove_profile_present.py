# Generated by Django 3.2.17 on 2023-02-09 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_profile_st'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='present',
        ),
    ]