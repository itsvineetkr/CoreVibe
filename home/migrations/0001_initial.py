# Generated by Django 5.0.6 on 2024-06-21 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDailyStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('data', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='UserGoals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('data', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='UserStaticStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('data', models.JSONField(default=list)),
            ],
        ),
    ]