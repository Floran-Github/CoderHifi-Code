# Generated by Django 3.0.7 on 2021-03-28 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recurit', '0002_auto_20210328_1021'),
        ('users', '0004_auto_20210328_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='languages_prefer',
            field=models.ManyToManyField(blank=True, default=None, to='recurit.language_category'),
        ),
    ]