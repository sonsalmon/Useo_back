from django.db import models

from books.models import Book,ReadingRelation


# Create your models here.


class Note(models.Model):
    reading_relation = models.ForeignKey(to=ReadingRelation, null=False, on_delete=models.CASCADE)
    content = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)