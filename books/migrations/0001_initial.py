# Generated by Django 4.2.5 on 2023-10-05 02:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posixpath


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "isbn",
                    models.CharField(max_length=13, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=50)),
                ("author", models.CharField(max_length=30)),
                ("description", models.TextField(default="")),
                ("publisher", models.CharField(max_length=30)),
                ("publish_date", models.DateField()),
                (
                    "cover_image",
                    models.ImageField(
                        blank=True, upload_to=posixpath.join, verbose_name="표지 이미지"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReadingRelation",
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
                (
                    "reading_state",
                    models.CharField(
                        choices=[
                            ("reading", "읽는 중이에요"),
                            ("later", "읽을 예정이에요"),
                            ("pause", "잠시 멈췄어요"),
                            ("quit", "읽다 그만뒀어요"),
                            ("finish", "다 읽었어요"),
                            ("never", "읽지 않을 거에요"),
                        ],
                        max_length=32,
                    ),
                ),
                ("reading_duration", models.DurationField()),
                ("add_date", models.DateField()),
                ("rate", models.FloatField()),
                (
                    "book_isbn",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="books.book"
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
