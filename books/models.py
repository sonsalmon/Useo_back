import os

from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from users.models import User


# Create your models here.


class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True, ) ### validator 설정하기!!
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    description = models.TextField(default='')
    publisher = models.CharField(max_length=30)
    publish_date = models.DateField()
    cover_image = models.ImageField(verbose_name='표지 이미지', upload_to=os.path.join,blank=True)

class ReadingRelation(models.Model):
    class ReadingState(models.TextChoices):
        READING = "reading", "읽는 중이에요"
        later ='later', '읽을 예정이에요'
        pause = 'pause', '잠시 멈췄어요'
        quit = 'quit', '읽다 그만뒀어요'
        finish = 'finish', '다 읽었어요'
        never = 'never', '읽지 않을 거에요'

    user_id = models.ForeignKey(to=User,null=False,on_delete=models.CASCADE,)
    book_isbn = models.ForeignKey(to=Book,null=False,on_delete=models.CASCADE,)
    reading_state = models.CharField(choices=ReadingState.choices, max_length=32)
    reading_duration = models.DurationField()
    add_date = models.DateField()
    rate = models.FloatField()
