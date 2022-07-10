from django import forms
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .validators import validate_letters  

class yellow_green_letters_field(forms.CharField):
    def validate(self, input_letters):
        yellow_gray_reg = r"^[ㄱ-ㅣ]{0,1}(,[ㄱ-ㅣ]){0,20}$"
        regex = re.compile(yellow_gray_reg)
        
        if not regex.match(input_letters):
            print("error")
            raise ValidationError(_('잘못된 입력입니다!'), code = 'invalid_input')
        
        super().validate(input_letters)


class SearchWordForm(forms.Form):

    yellow_letters = forms.CharField(label='Yellow Letters', required=False, validators=[validate_letters])
    gray_letters = forms.CharField(label='Gray Letters', required=False)

    green_letters_1 = forms.CharField(label='Green Letters_1', required=False)
    green_letters_2 = forms.CharField(label='Green Letters_2', required=False)
    green_letters_3 = forms.CharField(label='Green Letters_3', required=False)
    green_letters_4 = forms.CharField(label='Green Letters_4', required=False)
    green_letters_5 = forms.CharField(label='Green Letters_5', required=False)
    green_letters_6 = forms.CharField(label='Green Letters_6', required=False)

    '''
    def is_valid(self):
        yellow_gray_reg = r"^[ㄱ-ㅣ]{0,1}(,[ㄱ-ㅣ]){0,20}$"
        regex = re.compile(yellow_gray_reg)
        print(self.data)
        print(type(self.data))
        if not regex.match(self.data.__getitem__(yellow_letters)):
            raise ValidationError( _('%(yellow_letters)는 잘못된 입력입니다! 콤마로 구분된 한글 자모를 입력해주세요!'), code = 'invalid yellow_letters', params = {'yellow_letters': self.yellow_letters},)
        return super().is_valid()
    '''
