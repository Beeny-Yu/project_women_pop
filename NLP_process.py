import pandas as pd
m = pd.read_csv('man.csv') #남자 랭킹
w = pd.read_csv('woman.csv') #여자 랭킹

pip install nltk #자연어 처리 패키지

#자연어처리 패키지 불러오고 + 설치되었는지 버전 확인
import nltk 
nltk.__version__

#자연어처리 패키지 불러오고 + 설치되었는지 버전 확인
import konlpy 
konlpy.__version__

#가사 컬럼 값을 리스트로 변환
m_lyrics = m['Lyric'].tolist() 
w_lyrics = w['Lyric'].tolist()

#스트링으로 변환
for i in range(len(m_lyrics)):
    m_lyrics[i] = str(m_lyrics[i])
for i in range(len(w_lyrics)):
    w_lyrics[i] = str(w_lyrics[i])

#” “.join( list ) : 리스트에서 문자열으로
m_lyrics = ''.join(m_lyrics)
m_lyrics[:100000]
w_lyrics = ''.join(w_lyrics)
w_lyrics[:100000]

from konlpy.tag import Twitter
from konlpy.tag import Okt 
twitter = Twitter()
okt = Okt()
m_sample = twitter.pos(m_lyrics, norm=True)
w_sample = twitter.pos(w_lyrics, norm=True)

# 정규화 및 어근화를 마치고 품사 태깅까지 마친 상태에서,
# 조사, 어미, 구두점을 제외한 나머지 단어들을 모두 word_cleaned 리스트에 담습니다.
# 이 때에는 여러번 나온 단어들도 복수 허용되어 여러번 리스트에 담기게 됩니다.

# 유의미한 의미를 갖고 있지 않은 단어를 제외할 수 있습니다.
del_list = ['하다', '있다', '되다', '이다', '돼다', '않다', '그렇다', '아니다', '이렇다', '그렇다', '어떻다'] 

m_word_cleaned = []
for word in m_sample:
    if not word[1] in ["Josa", "Eomi", "Punctuation", "Foreign"]: # Foreign == ", " 와 같이 제외되어야할 항목들
        if (len(word[0]) != 1) & (word[0] not in del_list): # 한 글자로 이뤄진 단어들을 제외 & 원치 않는 단어들을 제외
            m_word_cleaned.append(word[0])
        
m_word_cleaned

del_list = ['하다', '있다', '되다', '이다', '돼다', '않다', '그렇다', '아니다', '이렇다', '그렇다', '어떻다'] 

w_word_cleaned = []
for word in w_sample:
    if not word[1] in ["Josa", "Eomi", "Punctuation", "Foreign"]: # Foreign == ", " 와 같이 제외되어야할 항목들
        if (len(word[0]) != 1) & (word[0] not in del_list): # 한 글자로 이뤄진 단어들을 제외 & 원치 않는 단어들을 제외
            w_word_cleaned.append(word[0])
        
w_word_cleaned

word_dic = {}

for word in m_word_cleaned:
    if word not in word_dic:
        word_dic[word] = 1 # changed from "0" to "1"
    else:
        word_dic[word] += 1
        
m_word_dic = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)

word_dic = {}

for word in w_word_cleaned:
    if word not in word_dic:
        word_dic[word] = 1 # changed from "0" to "1"
    else:
        word_dic[word] += 1
        
word_dic
# w_word_dic = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)

pip install wordcloud

pip install matplotlib

from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
import platform
%matplotlib inline    
#디스플레이 설정

import matplotlib 
from IPython.display import set_matplotlib_formats 

# set_matplotlib_formats('retina') 화면 흐린거 선명하게 설정

matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.family'] = "AppleGothic"


wordcloud = WordCloud(font_path='/Library/Fonts/AppleGothic.ttf',
                      background_color='white',colormap = "Accent_r", 
                      width=1500, 
                      height=1000,
                      max_words = 2000,
                      ).generate_from_frequencies(word_dic) 

plt.figure(figsize=(10,10))
plt.imshow(wordcloud) 
plt.axis('off') 
plt.show()
