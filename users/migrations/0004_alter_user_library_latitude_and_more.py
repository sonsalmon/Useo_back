# Generated by Django 4.2.5 on 2023-11-11 18:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_library_latitude_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="library_latitude",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="library_longitude",
            field=models.FloatField(blank=True, null=True),
        ),
    ]