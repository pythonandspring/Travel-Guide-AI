# Generated by Django 5.0 on 2025-01-06 12:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('travel_preferences', models.CharField(blank=True, default='', max_length=350, null=True)),
                ('favorite_destinations', models.TextField(blank=True, default='', null=True)),
                ('languages_spoken', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('budget_range', models.CharField(blank=True, default='', max_length=350, null=True)),
                ('interests', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
