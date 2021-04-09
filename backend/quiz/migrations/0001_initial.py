# Generated by Django 3.0.7 on 2021-03-28 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='quizcourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='quizLevels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('level', models.CharField(choices=[('Éasy', 'easy'), ('Medium', 'medium'), ('Hard', 'Hard')], max_length=100)),
                ('quizCourse_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quizcourse')),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.CharField(max_length=100, unique=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quizLevels')),
            ],
        ),
        migrations.CreateModel(
            name='answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.CharField(max_length=1000, unique=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('questionid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
            ],
        ),
    ]
