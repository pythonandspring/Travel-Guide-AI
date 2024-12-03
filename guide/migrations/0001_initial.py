# Generated by Django 5.0 on 2024-12-01 17:45

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
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('speciality', models.TextField()),
                ('attractions', models.TextField()),
                ('location_url', models.URLField()),
                ('nearest_cities', models.TextField()),
                ('state', models.CharField(max_length=100)),
                ('airports', models.TextField()),
                ('railway_stations', models.TextField()),
                ('road_distance', models.TextField()),
                ('images', models.ImageField(blank=True, null=True, upload_to='place_images/')),
                ('super_guide', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_places', to='guide.guide')),
            ],
        ),
        migrations.AddField(
            model_name='guide',
            name='assigned_places',
            field=models.ManyToManyField(related_name='guides', to='guide.place'),
        ),
    ]
