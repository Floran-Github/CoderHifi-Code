# Generated by Django 3.0.7 on 2021-05-19 20:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizapp', '0003_auto_20210517_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizlevels',
            name='peoplePassed',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]