from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Word
from django.views.generic.edit import FormView
from finder.forms import SearchWordForm
from plotly.offline import plot
import plotly.graph_objs as go
from django.db.models import Count
import plotly.express as px

class SearchFormView(FormView):
    form_class = SearchWordForm
    template_name = "finder/word_list.html"
        
    def get_data(self, word_list):
        words_count = word_list.count()
        letter_count = []
        letter_ratio = []
        letter = []

        for i in range(6):
            field = 'letter' + str(i+1)
            freq = word_list.values(field).annotate(letter_count = Count(field)).order_by('-letter_count')[:5]
            letter_count.append(len(freq))
            letter_ratio.extend([(f['letter_count']/words_count) * 100  for f in freq])
            letter.extend([f[field] for f in freq])
        
        return letter_count, letter_ratio, letter
       

    def make_plot(self, letter_count, letter_ratio, letter):
        y = []
        x = []
        
        for i, count in enumerate(letter_count):
            y.extend([6-i for j in range(count)])
            x.extend([j for j in range(count)])


        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x, y=y, text=letter, mode='text',
            textfont = {
                "size":letter_ratio    
            }
        ))
        
        
        fig.update_layout( 
            
            title={
                'text': "위치별 많이 등장하는 낱말",
                'xanchor': 'center',
                'x': 0.5
            },
            
            xaxis={
                'tickmode': 'array',
                'tickvals': [0,1,2,3,4,5],
                'ticktext': ['1위', '2위', '3위', '4위', '5위']
            },
            yaxis={
                'tickmode': 'array', 
                'tickvals': [6,5,4,3,2,1],
                'ticktext': ['첫번째 글자', '두번째 글자', '세번째 글자', '네번째 글자', '다섯번째 글자', '여섯번째 글자']
            }
        )
        
        plot_div = plot({'data': fig}, output_type='div')
        
        return plot_div


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
        
        #bubble chart 그리기 with plotly
        letter_count, letter, letter_ratio = self.get_data(word_list)
        
        plot_div = self.make_plot(letter_count, letter, letter_ratio) 
        
        context = {'word_list': word_list, 'form': form, 'plot_div': plot_div}
        return render(self.request, self.template_name, context)


