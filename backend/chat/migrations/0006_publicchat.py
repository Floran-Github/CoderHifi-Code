# Generated by Django 3.0.7 on 2021-05-02 15:43

import chat.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_discussionpanel_courseid'),
        ('chat', '0005_auto_20210414_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_for_chat', models.CharField(default=chat.models.generate, max_length=10, unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('messages', models.ManyToManyField(blank=True, to='chat.Message')),
            ],
        ),
    ]
