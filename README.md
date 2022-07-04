# JD 예측 서비스
직무명세서 (Job Description)에 기술된 포지션, 주요 업무, 자격요건, 우대사항에 가장 알맞는 직무를 예측하는 서비스 입니다.

구성
* `jd`: 데이터 전처리, 예측 모델 패키지
* `backend`: 모델 서빙, API 서비스

## 예시
### Sign Up
```bash
curl -X 'POST' \
  $JD_SERVICE_HOST/user/signup \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "string"
}'

# response
{"email":"user@example.com","id":1}%
```
### Login
```bash
curl -X 'POST' \
  $JD_SERVICE_HOST/user/login \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "string"
}'

# response
# {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidXNlckBleGFtcGxlLmNvbSIsImV4cGlyZXMiOjE2MjQzMzM0NDUuNzAwNjE5fQ.NmlsQxjaXpg5UD_RZgV9IvkyzeWRIEuE9aRP3QJP7Nk"}%
```
### Prediction
```bash
curl -X 'POST' \
  $JD_SERVICE_HOST/predict \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidXNlckBleGFtcGxlLmNvbSIsImV4cGlyZXMiOjE2MjQzMzM0NDUuNzAwNjE5fQ.NmlsQxjaXpg5UD_RZgV9IvkyzeWRIEuE9aRP3QJP7Nk' \
  -H 'Content-Type: application/json' \
  -d '{
        "wd_id": 42,
        "position": "머신러닝 엔지니어",
        "main_tasks": "딥러닝 백엔드 서비스 개발 및 유지보수\n",
        "requirements": "백엔드 프레임워크 (Django, Node.js 등등)를 기반으로 한 백엔드 서비스 개발 경험\n머신러닝에 대한 이해\n데이터베이스 구축 경험",
        "preferred_points": "딥러닝 프로젝트 경험"
}'

# response
# {"prediction":"개발"}%
```
## 설치
프로젝트의 `./script` 에 위치한 `install_dependencies`을 실행하여 패키지와 의존성을 설치 및 해결합니다.

호환성
* Linux (Ubuntu 20.04): python==3.8
* Windows 10: python 3.8, 3.9

## JD 예측하기
### 데이터 탐색
원본 데이터의 구성
* `wd_id`: jd의 ID
* `position`: 직무의 포지션 이름
* `main_tasks`: 주요 업무
* `requirements`: 자격 요건
* `preferred_points`: 우대사항
* `category`: 직무 카테고리


```python
import jd

raw_data = jd.util.load_json('./data/jd/raw_data.json')

print(raw_data[0])

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
```

주어진 `position`, `main_tasks`, `requirements`, `preferred_points`를 입력 데이터로, `category`를 레이블로 지정했습니다. 모델이 주어진 텍스트의 단어에서 context를 포착할 수 있을 것으로 예상했으며 단어만을 입력 데이터로 활용하기 위해 토큰화를 수행합니다. 
### 데이터 전처리
#### 토큰화
`Kiwi`의 `analyze`로 파악된 문장의 단어에서 예측을 하는데 중요한 형태소 유형인 일반명사 (NNG), 고유명사 (NNP) 그리고 영어 단어 (SL) 유형의 단어만을 추출하여 기존의 문장을 대체합니다. 대체되는 방식은 기존 문장의 `position`, `main_tasks`, `requirements`그리고 `preferred_points`에 대한 형태소 분석 및 추출 후 이들을 하나로 합칩니다.

```python
# 토큰화 예시
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

jd.data.tokenize_n_save_jd_data()
```
#### Word2Vec 모델 학습 및 저장
토큰화된 단어들에 대한 word vector를 생성하여 모델의 입력에 사용될 수 있도록 합니다. Word2Vec 모델을 학습하여 단어에 해당하는 정수 인덱스를 반환할 수 있거나 단어에 대한 가중치를 활용할 수 있도록 합니다.

#### 예측 모델
```python
    model = Sequential()
    # 임베딩 레이어
    model.add(layers.Embedding(input_dim=vocab_size,
                               output_dim=embedding_size,
                               weights=[w2v_weights],
                               input_length=input_maxlen,
                               mask_zero=True,
                               trainable=False,
                               name='embedding'))

    model.add(layers.Bidirectional(layers.LSTM(100)))
    model.add(layers.Dense(num_categories, activation='softmax', name='prediction'))
```
**임베딩 레이어**

단어를 word vector에 해당하는 가중치로 변환합니다.

```python
>>> w2v = jd.load_jd_text_model(model_type='word2vec')
load jd text model: path of the Word2Vec model is not set. set to the default value.
load 'word2vec' model successfully
>>> w2v_weights = w2v.wv.vectors
>>> vocab_size, embedding_size = w2v_weights.shape
>>> print(vocab_size, embedding_size)
5425 100
```
`vocab_size`는 모든 단어의 개수, `embedding_size`는 word vector의 벡터 크기를 의미합니다.

**Bi-directional LSTM**

데이터로 주어진 각 단어들을 통해 예측 feature를 생성하는 레이어 입니다. 

다음은 양방향 LSTM의 특징입니다.
> RNN이나 LSTM은 입력 순서를 시간 순대로 입력하기 때문에 결과물이 직전 패턴을 기반으로 수렴하는 경향을 보인다는 한계가 있다. 이 단점을 해결하는 목적으로 양방향 순한신경망(Bi-RNN)이 제안되었다. Bi-RNN은 기존의 순방향에 역방향을 추가하여, 은닉층에 추가하여 성능을 향상시켰다.
 그러나 데이터 길이가 길고 층이 깊으면, 과거의 정보가 손실되는 단점이 있다. 이를 극복하기 위해 제안된 알고리즘이 양방향 LSTM이다. (Ko et al., 2018)

단방향 일 때 한쪽 방향으로 수렴한다면 모델이 단어의 유사성을 파악하는데 방해가 될 것으로 생각해 양방향 LSTM으로 이를 해결하려 했습니다.

**Dense Layer**

양방향 LSTM이 생성한 feature에서 클래스에 해당하는 예측 결과를 나타냅니다.
