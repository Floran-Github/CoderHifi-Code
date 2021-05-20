# Generated by Django 3.0.7 on 2021-05-19 21:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_recruiter_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiter_profile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message="Entered mobile number isn't in a right format!", regex='^[0-9]{10,15}$')]),
        ),
    ]
