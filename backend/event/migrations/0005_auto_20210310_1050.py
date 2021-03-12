# Generated by Django 3.0.7 on 2021-03-10 05:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0004_auto_20210310_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='userEnrolled',
            field=models.ManyToManyField(blank=True, default=None, related_name='enrolled_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
