# Generated by Django 3.0.7 on 2021-03-05 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='project',
        ),
    ]
