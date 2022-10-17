# 공부로그 프로젝트 SA

# **B3 팀**

- 팀명 : 비상 ( b3 = 비상 = 우리는 현재 비상사태 입니다. = 내배캠이 끝나면 비상하겠습니다.)
- 팀장 : 이원채, 김민수
- 팀원 : 강기훈, 김경민, 현준호

## 프로젝트 이름 - [ **Stadying (스태딩) ]\*\*

stay와 study의 합성어로 자리에 머물러 공부를 한다는 의미로, 자리에 앉아 공부하는 사람을 인식해 주는 프로그램의 목적에 맞게 이름을 지었다.

## 프로젝트 목적

프로젝트 이름

- 카메라 앞에 앉아 공부중인 사람을 인식하여 자동으로 공부 중 여부를 확인하여 로그를 남기도록 한다.

서비스를 이용하는 사용자가 공부에 집중 할 수 있도록 공부 집중 시간을 기록하고 집중한 시간에 무엇을 하였는지 메모로 남길 수 있는 서비스를 구현하고 자 프로젝트를 계획했다.

- 프로젝트 역할
  - 강기훈
    - 회원가입 기능
    - 로그인
  - 김경민
    - 공부 로그 & 머신러닝 연동
    - 프로필 프론트
  - 김민수
    - SNS연동 로그인
    - 이메일 인증
  - 이원채
    - SNS연동 로그인
  - 현준호
    - 공부 로그 & 머신러닝 연동
    - 메인 화면 프론트

## Wireframe

![login.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/32a5eadf-2f33-4f89-b0b2-c4f3554d6c6e/login.jpg)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6a825726-38ae-4faa-912d-fa747db49e9d/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ff66d614-fb03-47b7-96ac-e96d32be02ab/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/890f76ce-db03-47de-8993-d44f80adfeca/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/47cb6365-42ea-4537-8a83-664e52c5dbb2/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/eb57150e-5148-4de2-a12f-cd554747fb34/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/10c30d4f-4dd6-4792-9863-0e67e747d7e4/Untitled.png)

## ERD

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/04d8a2c3-d66a-4468-b77a-f2689c140644/Untitled.png)

## 기능

- 회원가입, 로그인, 로그아웃
- 정보 수정, 비밀번호 변경
- 공부 로그 자동 기록

## User API

| 기능                               | method | url                          | request | response                          | 비고 |     |
| ---------------------------------- | ------ | ---------------------------- | ------- | --------------------------------- | ---- | --- |
| 회원가입                           | GET    | /user/join                   |         | join.html                         |      |     |
|                                    | POST   | /user/join                   |         |                                   |      |     |
| 로그인                             | GET    | /user/login                  |         | login.html                        |      |     |
|                                    | POST   | /user/login                  |         |                                   |      |     |
| 로그아웃                           | GET    | /user/logout                 |         | login.html                        |      |     |
|                                    |        |                              |         |                                   |      |     |
| 정보수정                           | GET    | /user/update/<int:user_id>   |         | user/update.html                  |      |     |
| 정보수정                           | POST   | /user/update/<int:user_id>   |         |                                   |      |     |
| 비밀번호변경                       | GET    | /user/change_password        |         | change_password.html              |      |     |
| 비밀번호변경                       | POST   | /user/change_password        |         |                                   |      |     |
| 이메일 인증 비밀번호 리셋          | GET    | /user/password_reset         |         | user/reset_password.html          |      |     |
|                                    | POST   | /user/password_reset         |         |                                   |      |     |
| 이메일 인증 비밀번호 리셋 완료알림 | GET    | /user/reset_password_done    |         | user/reset_password_done.html     |      |     |
|                                    | POST   | /user/reset_password_done    |         | user/login.html                   |      |     |
| 이메일 인증 비밀번호 리셋 결정     | GET    | /user/reset_password_confirm |         | /user/reset_password_confirm.html |      |     |
|                                    | POST   | /user/reset_password_confirm |         | /user/login/html                  |      |     |
| 회원탈퇴                           | GET    | /user/delete                 |         | user/delete.html                  |      |     |
|                                    | POST   | /user/delete                 |         | user/login.html                   |      |     |

## Service API

| 기능           | Method | URL                        | Request | Response          | 비고     |
| -------------- | ------ | -------------------------- | ------- | ----------------- | -------- |
| 회원 프로필    | GET    | /profile/<int:user_id>     |         | user/profile.html |          |
| 회원 로그 메모 | POST   | /profile/memo/<int:log_id> |         |                   | 추가기능 |
|                |        |                            |         |                   |          |
| 공부 시작      | GET    | /study/start               |         | -                 |          |
| 공부 종료      | GET    | /study/end                 |         | -                 |          |
|                |        |                            |         |                   |          |
| 공부 참여 체크 | GET    | /study/check               |         | -                 |          |
