# Generated by Django 3.0.7 on 2021-03-26 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20210325_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='content_name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]