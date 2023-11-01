# 모듈 임포트 선언
import os
import numpy as np
import pandas as pd

import re, unicodedata
from string import whitespace


from konlpy.tag import Okt
from gensim import corpora
from gensim.models import LdaModel, TfidfModel, CoherenceModel





# 크롤링 & 클렌징한 csv 파일 불러오기
df = pd.read_csv(r'C:\Users\User\Documents\Tesla_data\news_data_suyeon\2022_01_news_data.csv')

# 형태소 분석기 초기화
okt = Okt()

# 불용어 리스트 정의
stop_words = ['월', '위', '일', '억', '년', '원', '지난해', '를', '것', '등','차','올해','챗','위', '가', '조', '의', '및','약','수','주','기자',
              '만','이','중','말','마하','미','거','게','고','분','때문','때','더','점','씨','전','개','디','은','론','닉','키','김','책','그',
              '팀','스케','용','닉스', '이번', '그룹', '현지', '로이터', '전국', '하나', '루', '중이', '경찰', '자기', '확인', '운동', '남성', '청원', '창',
              '확', '집', '전달', '토크', '륜', '의학', '거주', '곳', '소', '기', '재', '하이', '초', '공간', '배포', '총','무단', '이마트', '대구',
              '저작권', '강동', '수다', '뉴스', '줌', '텍사스', '헬', '대신', '이름', '텍', '텍사스주','중산', '생수', '엠씨', '왜', '회장',
              '플로리다', '캘리포니아주', '약관', '본사', '건', '장기', '감염증', '캐릭터', '달이', '김혜민','순', '발', '스틱'
              '마스터', '산', '강원도', '부분', '주인', '알렉스', '제', '좀', '네', '보', '로직', '루다', '대한', '기업', '뉴욕', '가장',
              '선', '타이', '커피', '에브리싱', '명의', '베이커', '크루', '스프링', '완', '타고', '세션', '에스', '명', '이메일', '사업자',
              '개사', '만점', '대성', '데일리안', '킥', '수단', '부문', '플라잉', '별', '날', '장',  '행차', '기록', '백화점', '대비',
              '로', '달', '대표', '업체', '사업', '미래','계획', '세계', '회사', '업계', '시간', '예상', '사', '로', '볼', '걸', '수도', '저',
              '기존', '통해', '관련', '현재', '지난', '시장', '카','그룹', '차량', '협업', '서명', '바이', '산', '파이낸셜 뉴스',
              '대로', '전체', '고객', '공개', '서울', '이상', '아이오', '적용', '예정', '상황', '얘기', '정도', '안', '사실', '사람',
              '예스', '교수', '게임', '아이', '선', '대비', '며', '업종', '뉴시스', '하나', '좀', '경우', '재개', '부분', '가지', '계속', '오늘',
              '이후', '보도', '제','총', '가장', '제프', '억만장자', '최고', '부자','창업', '조스', '최대', '지급','박', '대해', '며', '영상', '자신',
              '국고', '차등', '위해', '미만', '이상', '경우', '개편', '일부', '지금', '생각', '우리', '요', '또', '앵커', '정치', '후보', '오늘', '안',
              '최근', '응답', '리움', '정부', '대표', '대통령', '국민', '면', '부산', '문', '장관', '회의', '사회', '주택', '제', '힘', '민주당', '오',
              '최근', '요', '와이드', '지리', '목표']

# 텍스트 데이터를 리스트로 변환
documents = df['content'].tolist()

# 각 문서를 형태소 분석 및 토큰화하고 불용어 제거
tokenized_documents = []
for document in documents:
    # 형태소 분석 수행 후 명사만 선택 (원하는 형태소 선택 가능)
    tokens = [word for word, pos in okt.pos(str(document)) if pos in ['Noun'] and word not in stop_words]
    tokenized_documents.append(tokens)

# 사전 (Dictionary) 생성
dictionary = corpora.Dictionary(tokenized_documents)



# Tfidf 모델 생성
tfidf = TfidfModel(dictionary=dictionary)
corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_documents]


# LDA 모델 생성
lda_model = LdaModel(corpus, num_topics=30, id2word=dictionary, passes=15)


# LDA 모델 출력
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic #{idx}: {topic}")