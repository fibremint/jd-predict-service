# 데이터 전처리 및 모델 학습 과정

JD 데이터를 전처리와 예측 모델의 생성 및 학습을 제공하는 모듈인 `jd`를 이용하여 이루어집니다. 과정의 실행 이전에 데이터를 저장하고 읽어오는 경로에 대한 환경변수 `JD_SERVICE_PATH`를 지정해야 합니다.

## 과정 요약

프로젝트 루트에서 다음을 실행합니다.

```
# 환경변수 설정
import os
import jd

# 서비스 경로 환경변수 설정
os.environ['JD_SERVICE_PATH'] = os.getcwd()

# 원본 데이터를 토큰화하며 이를 저장
jd.data.tokenize_n_save_jd_data()

# 텍스트 데이터에 대한 모델 (Word2Vec) 학습 및 저장
jd.model.create_trained_jd_text_model(model_type='word2vec')

# LSTM 모델 학습 및 저장
jd.model.create_trained_lstm_model()
```

## 데이터 전처리

원본 데이터 `raw_data.json`을 읽어온 후 토큰화 하며 모델의 학습에 사용될 수 있도록 저장합니다.

```python
jd.tokenize_n_save_jd_data()
```

### tokenize_n_save_jd_data()

`load_json`으로 읽어온  `json` 타입의 데이터는 `dict`이며 `tokenize_jd_data`로 토큰화를 적용 및 직무의 유형을 데이터에서 분리합니다.


**jd.preprocess.text._filter_tokenized**(…)

`Kiwi`의 `analyze`로 파악된 문장의 단어에서 예측을 하는데 중요한 형태소 유형인 일반명사 (NNG), 고유명사 (NNP) 그리고 영어 단어 (SL) 유형의 단어만을 추출하여 기존의 문장을 대체합니다. 대체되는 방식은 기존 문장의 `position`, `main_tasks`, `requirements`그리고 `preferred_points`에 대한 형태소 분석 및 추출 후 이들을 하나로 합칩니다.


```python
import jd

raw_data = jd.util.load_json('./data/jd/raw_data.json')

print(raw_data[0])
'''
{'wd_id': 61852, 'position': '고객 경험(CX) 전략 매니
저 (신입/인턴)', 'main_tasks': '• 24시간 365일 운영되
는 로켓펀치와 집무실 고객 경험 관리\n• 고객 경험 사이
클을 모니터링 및 개선하기 위한 전략 수립 및 운영 Support\n•
 11 star experience를 달성하기 위한 고객 경험 설
계 Support\n(참고: 11 star experience https://www.
disquiet.tech/post/11-star-framework-01 )', 'req
uirements': '• 소셜 네트워크 또는 플랫폼 커뮤니티 등 온라인
 플랫폼 운영에 관심이 있으신 분\n• 온라인 결제 시스템 운영
에 관심이 있으신 분\n• Google Spreadsheet 등을 활용하
여 숫자와 데이터를 다루는데 익숙하신 분\n• 고객의 니즈
와 이슈를 빠르게 파악하고 해결책을 찾아낼 수 있는 능력
\n• 시스템 운영, 관리, 개선을 주도적으로 할 수 있는 분
\n• 구글 워크스페이스, 슬랙 등 업무 및 협업 도구 활용
능력', 'preferred_points': '• 회사와 함께 성장하고자
하는 의지를 가진 분\n• 다양한 이슈에 빠르게 대응하고
해결하실 수 있는 분', 'category': '경영, 비즈니스'}
'''
tokenized_jds, categories = jd.preprocess.tokenize_jd_data(raw_data)

print(tokenized_jds[0])
'''
['고객', '경험', '전략', '매니저', '신입', '인턴', '시
간', '운영', '로켓', '펀치', '집무실', '고객', '경험', 
'관리', '고객', '경험', '사이클', '모니터링', '개선', 
'전략', '수립', '운영', 'support', 'star', 'exper
ience', '달성', '고객', '경험', '설계', 'support',
 '참고', 'star', 'experience', '네트워크', '플랫폼',
 '커뮤니티', '온라인', '플랫폼', '운영', '관심', '온라인',
 '결제', '시스템', '운영', '관심', 'google', 'spread
sheet','활용', '숫자', '데이터', '고객', '니즈', '이슈'
, '파악', '해결책', '능력', '시스템', '운영', '관리', '개선
', '주도', '구글', '워크스페이스', '슬랙', '업무', '협
업', '도구', '활용', '능력', '회사', '성장', '의지', 
'다양', '이슈', '대응', '해결']
'''
# print(categories[0])
# '경영, 비즈니스'
```


토큰화가 이루어진 이후 토큰화된 jd 데이터와 이에 대한 카테고리를 저장합니다.

## JD 데이터에 대한 Word2Vec 모델 학습 및 저장

토큰화된 JD 데이터를 불러오고 Word2Vec 모델을 생성 및 이 데이터에 대해 학습을 수행하며 저장합니다.


```python
jd.create_trained_jd_text_model(model_type='word2vec')
```

### create_trained_jd_text_model(model_type=’word2vec’, …)

**load_tokenized_jd_data(…)**

기존에 토큰화된 jd 데이터를 불러옵니다.


**save_jd_{MODEL_TYPE}_model(…)**

모델을 학습 및 저장합니다. Word2Vec의 경우 vector의 사이즈는 100으로 설정했습니다.

## LSTM 모델 학습 및 저장

토큰화된 JD 데이터와 Word2Vec 모델을 불러옵니다. 데이터는 LSTM 모델의 학습 이전에 전처리를 수행합니다. LSTM 모델을 생성하며 전처리된 데이터로 학습을 수행, 이후 학습된 모델을 `SavedModel`로 저장하여 모델을 배포하는데 사용될 수 있도록 합니다.


```python
jd.create_trained_lstm_model()
```

### create_trained_lstm_model

**load_tokenized_jd_data()**

토큰화된 데이터를 불러옵니다.


**load_jd_text_model(model_type=’word2vec)**

학습된 Word2Vec 모델을 불러옵니다.


**w2v_preprocess_data(…)**

`_w2v_word_to_token`으로 단어를 Word2Vec의 word vector인 `w2v_model.wv`에 대응하여 index로 변경하며 대응할 수 없는 값은 0으로 대체합니다. 데이터는 `pad_sequences`로 학습 이전에 모든 데이터가 일정한 길이를 갖도록 합니다.


**transform_jd_categories(…)**

카테고리를 정수형의 값으로 변경합니다.


**create_lstm_model(word2vec_model=w2v_model, …)**

LSTM 모델을 생성합니다. 학습된 Word2Vec 모델은 LSTM 모델의 Embedding 레이어를 구성하는데 사용되며 이 레이어의 `input_dim`은 `w2v_model.wv`의 고유한 단어들의 개수(vocab_size)이며 `output_dim`은 vector의 크기(embedding_size)입니다.


```python
w2v = jd.load_jd_text_model()
w2v_weights = word2vec_model.wv.vectors
vocab_size, embedding_size = w2v_weights.shape
print(w2v_weights.shape)
# (5425, 100)

m = jd.model.create_lstm_model(num_categories=4, word2vec_model=w2v, input_maxlen=250)
m.summary()

#Model: "sequential"
#_________________________________________________________________
#Layer (type)                 Output Shape              Param #
#=================================================================
#embedding (Embedding)        (None, 250, 100)          542500
#_________________________________________________________________
#bidirectional (Bidirectional (None, 200)               160800
#_________________________________________________________________
#dense (Dense)                (None, 4)                 804
#=================================================================
#Total params: 704,104
#Trainable params: 161,604
#Non-trainable params: 542,500
#_________________________________________________________________
```

이후 학습된 모델은 `SavedModel ` 포맷으로 저장됩니다.
