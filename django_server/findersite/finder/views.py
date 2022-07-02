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
    #def def get_success_url(self):
        #return str()

    #입력 받은 변수 검색 
    def form_valid(self, form):
         
        success_url = '/result/'
        #green = form.cleaned_data['green_letters']
        yellow = form.cleaned_data['yellow_letters']
        gray = form.cleaned_data['gray_letters']
       
        #입력값 querystring으로 indexView에 전달
        if yellow or gray:
            self.success_url += "?"
        if yellow:
            self.success_url += ('yellow=' + yellow)
        if yellow and gray:
            self.success_url += ('&gray=' + gray)
        if not yellow and gray:
            self.success_url += ('gray=' + gray)

        print(yellow, gray)
        
        ''' 
        word_list = Word.objects.all()
    
        if yellow:
            word_list = Word.objects.yellow_letters(word_list, yellow)
        
        if gray:
            word_list = Word.objects.gray_letters(word_list, gray)
        
        if green:
            word_list = Word.objects.green_letters(word_list, green)
        
        context = {}
        '''
        #context['word_list'] = word_list
        #context['yellow_letters'] = yellow
        #context['gray_letters'] = gray
        
        return super().form_valid(form)
        #render(self.request, self.template_name, context)        

class IndexView(generic.ListView):
    form_class = SearchWordForm
    green = ['', '', '', 'ㄱ', '', '']

    #기본적으로 데이터 보여주는 함수
    def get_queryset(self):
        
        yellow = self.request.GET.get("yellow", '')
        gray = self.request.GET.get("gray", '')
        
        word_list = Word.objects.all()
    
        if yellow:
            word_list = Word.objects.yellow_letters(word_list, yellow)
        
        if gray:
            word_list = Word.objects.gray_letters(word_list, gray)
        
        #if self.green:
            #word_list = Word.objects.green_letters(word_list, self.green)
        
        return word_list
