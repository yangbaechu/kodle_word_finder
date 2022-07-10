import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_letters(input_letters):
    yellow_gray_reg = r"^[ㄱ-ㅣ]{0,1}(,[ㄱ-ㅣ]){0,20}$"
    regex = re.compile(yellow_gray_reg)
    if not regex.match(input_letters):
        print("error")
        raise ValidationError(_('잘못된 입력입니다!'), code = 'invalid_input')
        

