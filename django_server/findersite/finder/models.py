from django.db import models

class Word(models.Model):
    word_text = models.CharField(max_length=40)
    word_pieces = models.CharField(max_length=40)
    frequent = models.IntegerField(default=0)

    def __str__(self):
        return self.word_text

#쿼리에 적용할 수 있는 함수
class WordManager(models.Manager):
    #노란색 단어
    def yellow_letters(self, letters):
        
        def yellow_letter(letter, QuerySet):
            return QuerySet.filter(word_pieces__contains=letter)

        QuerySet = Word.objects.all()

        for l in letters:
            QuerySet = letter_exist(l, QuerySet)  

        return QuerySet
