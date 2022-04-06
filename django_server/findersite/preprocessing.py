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

#글자별 column 만들기
#final_words['word_pieces'] = list(final_words['word_pieces'])

#시리즈 만들 배열
index = []
letter1 = []
letter2 = []
letter3 = []
letter4 = []
letter5 = []
letter6 = []

for row in final_words.iterrows():
    index.append(row[0])
    
    letter1.append(row[1]['word_pieces'][0])
    letter2.append(row[1]['word_pieces'][1])
    letter3.append(row[1]['word_pieces'][2])
    letter4.append(row[1]['word_pieces'][3])
    letter5.append(row[1]['word_pieces'][4])
    letter6.append(row[1]['word_pieces'][5])
    
    #print(row[0][0])
    #letter1 = row['word_pieces'][0]
    #index = row.index()
    #print(f'letter_1: {letter_1}, index: {index}')
    #if index == 2:
        #break

#시리즈 만들기
final_words["letter1"] = pd.Series(data=letter1, index=index)
final_words["letter2"] = pd.Series(data=letter2, index=index)
final_words["letter3"] = pd.Series(data=letter3, index=index)
final_words["letter4"] = pd.Series(data=letter4, index=index)
final_words["letter5"] = pd.Series(data=letter5, index=index)
final_words["letter6"] = pd.Series(data=letter6, index=index)



#print(final_words.loc[3, 'word_pieces'][2])
#final_words['letter_1'] = final_words['word_pieces'][3]
#print(final_words.head())

#df to model
records = Word.objects.all()
records.delete()

word_records = final_words.to_dict('records')


model_instances = [Word(word_pieces=record['word_pieces'], word_text=record['word'], frequent=record['ranking'], letter1=['letter1'], letter2=['letter2'], letter3=['letter3'], letter4=['letter4'], letter5=['letter5'], letter6=['letter6']) for record in word_records]

Word.objects.bulk_create(model_instances)

#print(Word.objects.filter(id=32))
print(final_words.iloc[120:180, :])
#print(len(final_words))
