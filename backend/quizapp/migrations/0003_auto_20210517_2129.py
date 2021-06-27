# Generated by Django 3.0.7 on 2021-05-17 15:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizapp', '0002_userparticipated_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userparticipated',
            name='status',
        ),
        migrations.AddField(
            model_name='quizcourse',
            name='peoplePassed',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quizlevels',
            name='peoplePassed',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]