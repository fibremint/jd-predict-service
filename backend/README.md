# JD 서비스
FastAPI 기반으로 학습된 모델의 서빙, 사용자 인증을 수행합니다.

구성
* `serve_tf` 
  * 요청된 데이터의 전처리
  * ML 모델에 기반한 추론
  * 추론한 결과 반환
* `api`
  * JWT에 기반한 사용자 인증
  * DB 연동

`serve_tf`는 내부 네트워크 (localhost)에서만 접근할 수 있고 `api`는 외부에서 접근이 가능합니다. JWT token으로 인증된 inference request만 `serve_tf`의 추론 서비스로 전달하여 인증된 사용자만 추론 서비스에 요청할 수 있도록 구현했습니다.
