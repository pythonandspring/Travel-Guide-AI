# Generated by Django 4.1.3 on 2024-11-19 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_profile_budget_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='budget_range',
            field=models.FloatField(blank=True, default=0, max_length=50, null=True),
        ),
    ]