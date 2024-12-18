# Generated by Django 5.1.2 on 2024-11-23 05:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recommendations", "0004_rename_date_useractivity_timestamp_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="user",
        ),
        migrations.RemoveField(
            model_name="userpreferences",
            name="user",
        ),
        migrations.RenameField(
            model_name="savedrecommendation",
            old_name="date_saved",
            new_name="saved_at",
        ),
        migrations.RenameField(
            model_name="useractivity",
            old_name="timestamp",
            new_name="date",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="date_of_birth",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="profile_picture",
        ),
        migrations.RemoveField(
            model_name="recommendation",
            name="date_added",
        ),
        migrations.RemoveField(
            model_name="recommendation",
            name="image",
        ),
        migrations.RemoveField(
            model_name="recommendation",
            name="impact_level",
        ),
        migrations.AddField(
            model_name="customuser",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="metadata",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="tags",
            field=models.TextField(default="general"),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="user_rating",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="recommendation",
            name="category",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="recommendation",
            name="title",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="savedrecommendation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="useractivity",
            name="action",
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name="CarbonFootprint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("month", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Goal",
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
        migrations.DeleteModel(
            name="UserPreferences",
        ),
    ]
