# docker_supabase_study


## DB 모델링
+ member 테이블:
  - 이메일 (Primary Key)
  - 이름
  - 비밀번호

+ 민원분류 테이블:
  - id (serial, Primary Key)
  - 내용 (카테고리, 예: 공공민원, 건강/의료)

+ 민원내용 테이블:
  - 작성자 (Foreign Key, member 테이블의 이메일 참조)
  - 민원분류 (Foreign Key, 민원분류 테이블의 id 참조)
  - 작성날짜 (DATE)
  - 작성시간 (TIMESTAMP)
  - 민원내용 (TEXT) 



<b>** csv 파일로 모델이 실시간 처리예정 : 스키마 생성 필요없음 **</b>
+ chatbot 테이블:
  - 원천 질문 데이터 (TEXT) ** 인덱스 지정
  - 민원 ID (Foreign Key, 민원분류 테이블의 id 참조)
  - 로봇 답변 데이터 (TEXT)
  - category (varchar, 필터링 기준)


---
<h3> 동기와 비동기 처리 - 챗봇의 트래픽 처리 방법 ① </h3>
<img src= "
