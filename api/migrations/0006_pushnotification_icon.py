# Generated by Django 4.2.11 on 2024-05-02 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_pushnotification"),
    ]

    operations = [
        migrations.AddField(
            model_name="pushnotification",
            name="icon",
            field=models.CharField(default="", max_length=500),
            preserve_default=False,
        ),
    ]
