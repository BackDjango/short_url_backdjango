# 단축 URL 챌린지

## 💡 프로젝트 개요
- 단축 URL 서비스를 DRF로 구현
- 기한: 2024.05.07 ~ 20204.05.21
  - 중간 점검: 14일 (1주차)
  - 최종 발표: 21일 (2주차)

## 🚤 진행 방식
- 기능단위에 초점을 맞춰 개발하고 이슈 및 PR 생성
- 진행 하면서 추가되는 셋팅이 있다면 Initialize_Django에 개선하기
- 삽질 일기 작성 (노션 및 블로그)

## ⚙️ 구현 기능
- User
  - 회원가입
  - 로그인
  - token 재발급
  - 정보 조회
- 단축 URL
  - 생성
  - 리스트 조회
  - 삭제
  - 조회 (redirect)
  - 통계
- 환경변수 관리
- Logging 기능
- Swagger
- black

## 🔎 상세 내용
- 긴 url을 단축 url로 변경
    - url 생성시 만료 옵션을 추가하면 해당 만료일시 이후의 요청에는 응답하지 않음 (삭제처리)
    - 만료옵션이 있는 url에 대해 재 생성 요청을 하게 되는 경우 이전 옵션을 무시
- 단축 url 호출시 긴 url로 리다이렉트
- 만들어진 url 뒤에 '+' 를 붙이면 통계 기능 제공 (API)
    - 일간 조회수(최근 7일)
    - 전체 조회수
    - 전체 리퍼러별 조회수
        - 만료옵션이 있는 url에 대해 재 생성 요청을 하게 되는 경우 이전 옵션을 무시

## 🛠️ 구현 조건
- 코드 컨벤션 PEP8
- Python 3.11
- Django 5.0.4
- DRF 3.15.1
- CI (Jenkins or Github Action 등)
- CD (옵션)
- ORM
- DB (MySQL)
- 각 도메인(테이블)의 요소(필드)들은 자유
- 문서화 라이브러리
