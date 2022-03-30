import pandas as pd
from jamo import h2j, j2hcj
from collections import defaultdict

words = pd.read_csv("./word_list.csv", encoding='CP949', usecols=['순위', '단어', '품사'])

words = words.rename(columns = {'순위': 'ranking', '단어': 'word', '품사': 'word_class'})

noun_mask = (words.word_class == '명') | (words.word_class == '대') | (words.word_class == '고')
nouns = words.loc[noun_mask, :].copy()

#자모, 겹모음 분리
pieces_to_split = {'ㅔ':['ㅓ','ㅣ'], 'ㅐ':['ㅏ','ㅣ'], 'ㅒ':['ㅑ','ㅣ'], 'ㅘ':['ㅗ','ㅏ'], 'ㅚ':['ㅗ','ㅣ'], 'ㅙ':['ㅗ','ㅏ', 'ㅣ'], 'ㅝ':['ㅜ','ㅓ'], 'ㅞ':['ㅜ','ㅓ','ㅣ'], 'ㅟ':['ㅜ','ㅣ'], 'ㅢ':['ㅡ','ㅣ'], 'ㄲ':['ㄱ','ㄱ'], 'ㄸ':['ㄷ','ㄷ'], 'ㅉ':['ㅈ','ㅈ'], 'ㅃ':['ㅂ','ㅂ'], 'ㅆ':['ㅅ','ㅅ'], 'ㅄ':['ㅂ','ㅅ'], 'ㄺ':['ㄹ','ㄱ'], 'ㄻ':['ㄹ','ㅁ']}
nouns["word_pieces"] = ""

for i, row in enumerate(nouns.loc[:,'word']):
    pieces = j2hcj(h2j(row))
    p = 'ㅔ'
    
    for p in pieces_to_split:
        if p in pieces:
            pieces = pieces.replace(p, ''.join(pieces_to_split[p]))
            print(pieces)
    
    nouns.loc[i, 'word_pieces'] = pieces
print(nouns.loc[300:350, :])
