# Generated by Django 5.1.2 on 2024-12-02 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recommendations", "0015_alter_savedrecommendation_unique_together_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="savedrecommendation",
            name="completed",
            field=models.BooleanField(default=False),
        ),
    ]
