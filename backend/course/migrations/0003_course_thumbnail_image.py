# Generated by Django 3.0.7 on 2021-03-23 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20210323_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='thumbnail_image',
            field=models.ImageField(default='course_default.jpg', upload_to='course_thubnail'),
        ),
    ]
