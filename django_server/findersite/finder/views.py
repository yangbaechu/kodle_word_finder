from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Word

class IndexView(generic.ListView):
    model = Word   
    
