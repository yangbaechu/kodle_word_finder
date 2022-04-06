from django.db import models

class WordManager(models.Manager):
    
    #def get_queryset(self):
        #return super().get_queryset().filter(word_pieces[3] = 'ㄱ')

    #노란색 단어
    def yellow_letters(self, queryset, letters):
        
        def yellow_letter(letter, QuerySet):
            return QuerySet.filter(word_pieces__contains=letter)

        QuerySet = Word.objects.all()

        for l in letters:
            QuerySet = yellow_letter(l, QuerySet)  

        return QuerySet

class Word(models.Model):
    word_text = models.CharField(max_length=40)
    word_pieces = models.CharField(max_length=40)
    frequent = models.IntegerField(default=0)
    letter1 = models.CharField(max_length=5, default='')
    letter2 = models.CharField(max_length=5, default='')
    letter3 = models.CharField(max_length=5, default='')
    letter4 = models.CharField(max_length=5, default='')
    letter5 = models.CharField(max_length=5, default='')
    letter6 = models.CharField(max_length=5, default='')
    
    objects = WordManager()

    def __str__(self):
        return self.word_text


