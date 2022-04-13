from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Word
from django.views.generic.edit import FormView
from finder.forms import SearchWordForm

class SearchFormView(FormView):
    form_class = SearchWordForm
    template_name = "finder/word_list.html"

    #입력 받은 변수 검색 
    def form_valid(self, form):
        yellow = self.request.GET.get('yellow_letters', '')
        #form.cleaned_data['yellow_letters']
        gray = self.request.GET.get('gray_letters', '')
        green = False
        print(yellow, gray)
        #green = form.cleaned_data['green_letters']

        word_list = Word.objects.all()
    
        '''
        if yellow:
            word_list = Word.objects.yellow_letters(word_list, yellow)
        
        if gray:
            word_list = Word.objects.gray_letters(word_list, gray)
        
        if green:
            word_list = Word.objects.green_letters(word_list, green)
        '''
        context = {}
        context['word_list'] = word_list
        context['yellow_letters'] = yellow
        context['gray_letters'] = gray
        
        return super().form_valid(form)
        #return render(self.request, self.template_name, context)

class IndexView(generic.ListView):
    yellow = ['ㄴ','ㄹ']
    gray = ['ㅇ', 'ㅏ', 'ㅣ']
    green = ['', '', '', 'ㄱ', '', '']

    #기본적으로 데이터 보여주는 함수
    def get_queryset(self):
        
        word_list = Word.objects.all()
    
        if self.yellow:
            word_list = Word.objects.yellow_letters(word_list, self.yellow)
        
        if self.gray:
            word_list = Word.objects.gray_letters(word_list, self.gray)
        
        if self.green:
            word_list = Word.objects.green_letters(word_list, self.green)
        
        return word_list
