# Generated by Django 3.2.17 on 2023-02-09 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_profile_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='st',
            field=models.CharField(choices=[('pr', 'pr'), ('abs', 'abs'), ('late', 'late')], default='abs', max_length=20, null=True),
        ),
    ]