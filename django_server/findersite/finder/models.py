from django.db import models

class WordManager(models.Manager):
    
    #노란색 단어
    def yellow_letters(self, QuerySet, letters):
        
        def yellow_letter(letter, QuerySet):
            return QuerySet.filter(word_pieces__contains=letter)

        for l in letters:
            QuerySet = yellow_letter(l, QuerySet)  

        return QuerySet
    
    #회색 단어
    def gray_letters(self, QuerySet, letters):
        
        def gray_letter(letter, QuerySet):
            return QuerySet.exclude(word_pieces__contains=letter)

        for l in letters:
            QuerySet = gray_letter(l, QuerySet)  

        return QuerySet

    #초록색 단어
    def green_letters(self, QuerySet, letters):
        
        if letters[0] != '':
            QuerySet = QuerySet.filter(letter1__contains = letters[0])
        if letters[1] != '':
            QuerySet = QuerySet.filter(letter2__contains = letters[1])
        if letters[2] != '':
            QuerySet = QuerySet.filter(letter3__contains = letters[2])
        if letters[3] != '':
            QuerySet = QuerySet.filter(letter4__contains = letters[3])
        if letters[4] != '':
            QuerySet = QuerySet.filter(letter5__contains = letters[4])
        if letters[5] != '':
            QuerySet = QuerySet.filter(letter6__contains = letters[5])
        
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

