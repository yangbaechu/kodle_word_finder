from django.db import models

class Word(models.Model):
    word_text = models.CharField(max_length=40)
    word_pieces = models.CharField(max_length=40)
    frequent = models.IntegerField(default=0)
