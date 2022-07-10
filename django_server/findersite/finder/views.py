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
        print("form is valid") 
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
        
        #입력된 단어 검색
        word_list = Word.objects.all()
    
        if yellow[0] != '':
            word_list = Word.objects.yellow_letters(word_list, yellow)
        
        if gray[0] != '':
            word_list = Word.objects.gray_letters(word_list, gray)
        
        if green:
            word_list = Word.objects.green_letters(word_list, green)
        
        context = {'word_list': word_list, 'form':form}
        
        return render(self.request, self.template_name, context)


