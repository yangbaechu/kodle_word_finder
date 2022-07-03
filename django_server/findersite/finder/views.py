from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Word
from django.views.generic.edit import FormView
from finder.forms import SearchWordForm

class SearchFormView(FormView):
    form_class = SearchWordForm
    template_name = "finder/word_list.html"
    success_url = '/result/'
    
    #입력한 단어를 url 쿼리스트링에 추가
    def make_success_url(self, yellow, gray, green):
        #1. 단어를 letters에 모으기
        letters = []
        if yellow != '':
            letters.append("yellow=" + ','.join(yellow))
        if gray != '':
            letters.append("gray=" + ','.join(gray))

        for i, green_letter in enumerate(green):
            if green_letter:
                letters.append("green_" + str(i+1) + "=" + str(green_letter))
        
        #2. letters로 url 만들기
        for i, letter in enumerate(letters):
            if i == 0:
                self.success_url += '?'
            self.success_url += letter
            if i != len(letter) - 1:
                self.success_url += "&"
        return
    
    #입력 받은 변수 검색 
    def form_valid(self, form):
         
        #사용자가 입력한 변수 전달받고 배열로 변경
        yellow = form.cleaned_data['yellow_letters'].split(",")
        gray = form.cleaned_data['gray_letters'].split(",")
        
        green = []
        for i in range(6):
            field_name = "green_letters_" + str(i+1)
            if form.cleaned_data[field_name]:
                green.append(form.cleaned_data[field_name])
            else:
                green.append('')
       
        self.make_success_url(yellow, gray, green)
        
        return super().form_valid(form)

class IndexView(generic.ListView):
    form_class = SearchWordForm
    gray = []
    yellow = []
    green = []

    #기본적으로 데이터 보여주는 함수
    def get_queryset(self):
        
        #form에서 전한 데이터 받기
        self.yellow = self.request.GET.get("yellow", '').split(',')
        self.gray = self.request.GET.get("gray", '').split(',')
        self.green = []
        
        for i in range(6):
            field = 'green_' + str(i+1)
            if self.request.GET.get(field, '') == '':
                self.green.append('')
            else:
                self.green.append(self.request.GET.get(field, ''))
        
        
        print(self.yellow, self.gray, self.green)
        word_list = Word.objects.all()
    
        if self.yellow:
            word_list = Word.objects.yellow_letters(word_list, self.yellow)
        
        if self.gray:
            word_list = Word.objects.gray_letters(word_list, self.gray)
        
        if self.green:
            word_list = Word.objects.green_letters(word_list, self.green)
        
        return word_list
