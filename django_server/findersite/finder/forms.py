from django import forms

class SearchWordForm(forms.Form):
    yellow_letters = forms.CharField(label='Yellow Letters', required=False)
    gray_letters = forms.CharField(label='Gray Letters', required=False)

    green_letters_1 = forms.CharField(label='Green Letters_1', required=False)
    green_letters_2 = forms.CharField(label='Green Letters_2', required=False)
    green_letters_3 = forms.CharField(label='Green Letters_3', required=False)
    green_letters_4 = forms.CharField(label='Green Letters_4', required=False)
    green_letters_5 = forms.CharField(label='Green Letters_5', required=False)
    green_letters_6 = forms.CharField(label='Green Letters_6', required=False)
