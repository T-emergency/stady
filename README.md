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


![login](https://user-images.githubusercontent.com/113074274/196135459-ea184583-61e6-466c-8d05-51462f75d3a4.jpg)

![Untitled](https://user-images.githubusercontent.com/113074274/196135857-6dcbb025-ba38-4298-8dd9-e003e34cf101.png)

![Untitled 1](https://user-images.githubusercontent.com/113074274/196135871-dfcc32e2-e8ff-4f9d-913a-d859cba3da0d.png)

![Untitled 2](https://user-images.githubusercontent.com/113074274/196135891-76a2cdea-9963-4033-bd45-e40b212d69ed.png)

![Untitled 3](https://user-images.githubusercontent.com/113074274/196135902-cf115049-c1fe-4f50-a7f7-7be27a0069e7.png)

![Untitled 4](https://user-images.githubusercontent.com/113074274/196135914-00b696b9-37e8-4066-b5d2-ac583b8f2a56.png)

![Untitled 5](https://user-images.githubusercontent.com/113074274/196135922-c4de645e-ab53-478c-b227-15ad3ae95407.png)


## ERD

![Untitled 6](https://user-images.githubusercontent.com/113074274/196135948-aefaf871-dcaa-4a71-bfd8-5586497912e9.png)

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
