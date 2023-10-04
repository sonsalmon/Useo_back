from django.db import models

# Create your models here.


class Note(models.Model):
    user_id = models.ForeignKey(to='ReadingRelation', null=False, on_delete=models.CASCADE)
    content = models.TextField()
    add_date = models.DateField()
    last_modify = models.DateField()