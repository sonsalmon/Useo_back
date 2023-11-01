import os

from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from users.models import User


# Create your models here.


class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True, ) ### validator 설정하기!!
    title = models.CharField(max_length=50,null=True)
    author = models.CharField(max_length=30,null=True)
    description = models.TextField(default='',null=True)
    publisher = models.CharField(max_length=30,null=True)
    publish_date = models.DateField(null=True)
    cover_image = models.ImageField(verbose_name='표지 이미지', upload_to='books/cover',blank=True,null=True)

class ReadingRelation(models.Model):
    class ReadingState(models.TextChoices):
        READING = "reading", "읽는 중이에요"
        LATER ='later', '읽을 예정이에요'
        PAUSE = 'pause', '잠시 멈췄어요'
        QUIT = 'quit', '읽다 그만뒀어요'
        FINISH = 'finish', '다 읽었어요'
        NEVER = 'never', '읽지 않을 거에요'

    class Meta:
        constraints=[
            models.UniqueConstraint(
                name='unique_manager',
                fields=['user', 'book']

            )
        ]

    user = models.ForeignKey(to=User,null=False,on_delete=models.CASCADE,)
    book = models.ForeignKey(to=Book,null=False,on_delete=models.CASCADE,)
    reading_state = models.CharField(choices=ReadingState.choices, max_length=32)
    reading_duration = models.DurationField()
    add_date = models.DateField()
    rate = models.FloatField()
