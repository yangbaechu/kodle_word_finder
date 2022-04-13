from django import forms

class SearchWordForm(forms.Form):
    yellow_letters = forms.CharField(label='Yellow Letters')
    gray_letters = forms.CharField(label='Gray Letters')
