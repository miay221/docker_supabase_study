# docker_supabase_study


1. member 테이블:
이메일 (Primary Key)
이름
비밀번호

3. 민원분류 테이블:
id (serial, Primary Key)
내용 (카테고리, 예: 일반 행정, 공공의료)

4. 민원내용 테이블:
작성자 (Foreign Key, member 테이블의 이메일 참조)
민원분류 (Foreign Key, 민원분류 테이블의 id 참조)
작성날짜 (DATE)
작성시간 (TIMESTAMP)
민원내용 (TEXT)

5. chatbot 테이블:
원천 질문 데이터 (TEXT) ** 인덱스 지정
민원 ID (Foreign Key, 민원분류 테이블의 id 참조)
로봇 답변 데이터 (TEXT)
+ 원천 질문 데이터 벡터화 정보
