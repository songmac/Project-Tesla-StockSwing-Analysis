# -*- coding: utf-8 -*-
"""[colab]_(2)_Preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ny-VMjEDK3pyzyZZ8r-_IemR0aFNzhoL

#데이터 전처리 작업

## 데이터 정제 (Data Cleaning)
- 잡음, 부적합, 결측치를 수정하고 읽을 수 없는 요소 제거
- 형식의 일관성을 유지하고 적합한 포맷으로 변환

1. 잡음
   - 구간화 : 정렬된 데이터를 구간으로 분할
   - 회귀 : 회귀 분석을 통해 평활화
   - 군집화 : 유사한 값들을 그룹화

### git 설정

- git에 수집 된 데이터를 불려오기 위한 git clone 설정
"""

from google.colab import drive
drive.mount('/content/drive')

#csv 파일 불려오기 위한 깃 클론
!git clone https://github.com/maximin90/Team_SeSAC.git

# 디렉토리 변경
cd Team_SeSAC/

# git 접근권한 부여를 위한 git 계정 추가
!git config --global user.email "iove0103@naver.com"
!git config --global user.name "yumioh"

!git status

!git pull

#깃 커밋
!git add .
!git commit -m 'new : add merged data file'

#!git pull
#!git push origin ymNews

"""### 수집한 데이터인 cvs 파일 불려오기
- 매달 수집한 뉴스 데이터 병합하기
"""

#엑셀 파일 병합하기
filepath = f'/content/Team_SeSAC/yumi/data/'

#파일 경로
file_list = os.listdir(filepath)
#경로에 있는 모든 csv파일 리스트 불려오기
file_list_csv = [file for file in file_list if file.endswith('csv')]

#저장할 dataframe
merged_df = pd.DataFrame()

for file in file_list_csv:
  #read_excel기능으로 파일 읽음
  df = pd.read_csv(filepath + file, dtype='object')
  merged_df = merged_df.append(df)

#병합엑셀 파일 저장
merged_df.to_csv("/content/Team_SeSAC/yumi/data/[2023]_merge_news_data.csv",index=False, encoding='utf-8-sig')

merged_df.shape

import json
import pandas as pd
import numpy as np
import os

#데이터 수집한 파일 한개 들고 오기
filename = f'[2023_FEB]_news_data.csv'
meger_filename = f'[2023]_merge_news_data.csv'
#filepath = f'/content/Team_SeSAC/yumi/data/'+filename
filepath = f'/content/Team_SeSAC/yumi/data/'+meger_filename

df = pd.read_csv(filepath)
df.shape

"""### 결측지 제거 : 비어 있는 행 제거"""

df = df.dropna(axis=0)
df.shape
df.head(10)

"""### 목적에 맞는 정보 수집을 위해 불필요한 정보제거
- media(신문매체이름), Unnamed 열 제거
- 정규화를 통한 공백처리, 한글만 추출 등 부적합한 요소 제거
- 140자 이하 신문기사 내용 제외
- 1차 처리된 데이터 cvs파일로 저장

"""

df.drop(['media','Unnamed: 0'],axis=1,inplace = True)
df.shape
df.head(10)

import re, unicodedata
from string import whitespace

pattern_whitespace = re.compile(f'[{whitespace}]+')
# NaN 값을 빈 문자열로 대체
df['content_data'] = df['content'].fillna('').astype(str)

# 공백 처리 및 정규화
pattern_whitespace = re.compile(f'[{whitespace}]+')

df['content_data'] = df['content_data'].str.replace(
    pattern_whitespace, ' '
).map(lambda x: unicodedata.normalize('NFC', x)).str.strip()

def clean_byline(text):
    # byline
    pattern_email = re.compile(r'[-_0-9a-z]+@[-_0-9a-z]+(?:\.[0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_url = re.compile(r'(?:https?:\/\/)?[-_0-9a-z]+(?:\.[-_0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_others = re.compile(r'\.([^\.]*(?:기자|특파원|지난해|교수|서울|사진|작가|뉴스|대표|논설|고문|주필|부문장|팀장|장관|원장|연구원|이사장|위원|실장|차장|부장|에세이|화백|사설|소장|단장|과장|기획자|큐레이터|저작권|평론가|©|©|ⓒ|\@|\/|=|:앞쪽_화살표:|무단|전재|재배포|금지|\[|\]|\(\))[^\.]*)$')
    pattern_onlyKorean = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글과 띄어쓰기만 추출
    result = pattern_email.sub('', text)
    result = pattern_url.sub('', result)
    result = pattern_others.sub('.', result)
    result = pattern_onlyKorean.sub('',result)
    # 본문 시작 전 꺽쇠로 쌓인 바이라인 제거
    pattern_bracket = re.compile(r'^((?:\[.+\])|(?:【.+】)|(?:<.+>)|(?:◆.+◆)\s)')
    result = pattern_bracket.sub(' ', result).strip()
    return result
df['content_data'] = df['content_data'].map(clean_byline)

df.head(10)

#content 기사 길이가 140자 이하인 경우 제외
df = df.loc[df['content_data'].str.len() > 140]
df.shape

#cvs로 파일 저장
df.to_csv('/content/drive/MyDrive/핀테크 추천시스템/테슬라 프로젝트/tesla_data/telsa_preprosessing.csv',encoding='utf-8-sig')

"""### Counter 모듈을 이용하여 가장 많이 나오는 단어 추출"""

# 상위 10개 단어 추출 함수
def word_counter(wordArr):
  all_word = [word for words in wordArr for word in words]
  word_count = Counter(all_word)
  most_commos_words = word_count.most_common(20)
  return most_commos_words

from collections import Counter
#가장 많이 나오는 단어 추출
words_list = df['content_data'].str.split()
word_counter(words_list)

print(words_list[:10])

"""### 기사내용을 공백으로 토큰화
 - 토큰화는 단어별로 분리하는 단어 토큰화와 문자별로 분리하는 문장 토큰화로 구분

"""

from gensim import corpora

docs = df['content_data']

#공백으로 토큰화
tokenized_docs = []
for doc in docs:
  tokenized_docs.append(doc.split())

word_counter(tokenized_docs)

"""# 텍스트 분석

## LDA 모델링 (형태소 및 불용어 처리 전)
"""

id2word = corpora.Dictionary(tokenized_docs)
print(id2word)

for value in id2word:
  print(value, id2word[value])

corpus_TDM = []
for doc in tokenized_docs:
  #print(doc)
  result = id2word.doc2bow(doc)
  corpus_TDM.append(result)

corpus_TDM

from gensim.models import LdaModel, TfidfModel

tfidf = TfidfModel(corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]

n = 10 #토픽의 개수
lda = LdaModel(corpus=corpus_TFIDF,
               id2word=id2word,
               num_topics=n,
               random_state=100)

for t in lda.print_topics():
  print(t[0],":",t[1])

"""## LDA 모델링(형태소 및 불용화 처리 후)
 - okt 모듈을 이용한 형태소 분류

### mecab 설치
"""

# Commented out IPython magic to ensure Python compatibility.
#mecab 설치
!git clone https://github.com/SOMJANG/Mecab-ko-for-Google-Colab.git
# %cd Mecab-ko-for-Google-Colab/
!bash ./install_mecab-ko_on_colab_light_220429.sh

#konply install
#!pip install konlpy

"""### 형태소 처리
- mecab을 통해 형태소 단위로 나눔
"""

from konlpy.tag import Mecab

mecab = Mecab()
df['tokenized_content'] = df['content_data'].apply(lambda x: mecab.morphs(x))
df['tokenized_content']

"""### 품사부착 (PoS Tagging)
- 명사만 추출
- 최빈어를 조회하여 불용어 제거 대상 선정
"""

#명사만 분류 (nouns)
df['nouns_content'] = df['content_data'].apply(lambda x: mecab.nouns(x))

df['nouns_content'][:10]

"""### 불용어 처리(stopword)
- 자연어처리를 위해 불필요한 요소를 제거
- 최빈어 조회하여 불용어 제거 대상을 선정
"""

stop_words = ['월', '위', '일', '억', '년', '원', '지난해', '를', '것', '등','차','올해','챗'
              '위', '가', '조', '의', '및','약','수','주','기자','만','이','중','말','마하','미']

def remove_korean_stopwords(nouns_list):
    return [word for word in nouns_list if word not in stop_words]

words_list = df['nouns_content'].tolist()

clean_words = df['nouns_content'].apply(remove_korean_stopwords)
print('불용어 제거 후 : ', clean_words[:20])

# 최빈어를 조회하여 불용어 제거 대상 선정
most_common_tag = []
for token in clean_words:
  most_common_tag += token
Counter(most_common_tag).most_common(30)

id2word = corpora.Dictionary(clean_words)
print(id2word)

corpus_TDM = []
for doc in clean_words:
  #print(doc)
  result = id2word.doc2bow(doc)
  corpus_TDM.append(result)

corpus_TDM

from gensim.models import LdaModel, TfidfModel

tfidf = TfidfModel(corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]

n = 20 #토픽의 개수
lda = LdaModel(corpus=corpus_TFIDF,
               id2word=id2word,
               num_topics=n,
               random_state=100)

for t in lda.print_topics():
  print(t[0],":",t[1])