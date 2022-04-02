import os
import django

#Model 사용하기
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "findersite.settings")
django.setup()

import pandas as pd
from jamo import h2j, j2hcj
from collections import defaultdict
from finder.models import Word
import re

words = pd.read_csv("./word_list.csv", encoding='CP949', usecols=['순위', '단어', '품사'])

words = words.rename(columns = {'순위': 'ranking', '단어': 'word', '품사': 'word_class'})

is_noun = (words.word_class == '명') | (words.word_class == '대') | (words.word_class == '고')
nouns = words.loc[is_noun, :].copy()

#숫자 제거
p = re.compile('[0-9]')
nouns_without_num = []

for row in nouns.loc[:, 'word']:
    nouns_without_num.append(p.sub('', row))

nouns["word"] = nouns_without_num

#자모, 겹모음 분리
pieces_to_split = {'ㅔ':['ㅓ','ㅣ'], 'ㅐ':['ㅏ','ㅣ'], 'ㅒ':['ㅑ','ㅣ'], 'ㅘ':['ㅗ','ㅏ'], 'ㅚ':['ㅗ','ㅣ'], 'ㅙ':['ㅗ','ㅏ', 'ㅣ'], 'ㅝ':['ㅜ','ㅓ'], 'ㅞ':['ㅜ','ㅓ','ㅣ'], 'ㅟ':['ㅜ','ㅣ'], 'ㅢ':['ㅡ','ㅣ'], 'ㄲ':['ㄱ','ㄱ'], 'ㄸ':['ㄷ','ㄷ'], 'ㅉ':['ㅈ','ㅈ'], 'ㅃ':['ㅂ','ㅂ'], 'ㅆ':['ㅅ','ㅅ'], 'ㅄ':['ㅂ','ㅅ'], 'ㄺ':['ㄹ','ㄱ'], 'ㄻ':['ㄹ','ㅁ']}
nouns["word_pieces"] = ""


for i, row in nouns.iterrows():
    pieces = j2hcj(h2j(row['word']))

    for p in pieces_to_split:
        if p in pieces:
            pieces = pieces.replace(p, ''.join(pieces_to_split[p]))
    
    nouns.loc[i, 'word_pieces'] = pieces

is_six_letter = nouns.word_pieces.str.len() == 6
six_letter_nouns = nouns.loc[is_six_letter,:].copy()
final_words = six_letter_nouns.drop_duplicates(['word']).copy()
final_words.fillna(3000, inplace=True)

#df to model
word_records = final_words.to_dict('records')

model_instances = [Word(word_pieces=record['word_pieces'], word_text=record['word'], frequent=record['ranking']) for record in word_records]

Word.objects.bulk_create(model_instances)

print(Word.objects.filter(id=32))
#print(final_words.iloc[:50, :])
#print(len(final_words))
