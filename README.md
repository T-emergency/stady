# 공부로그 프로젝트 SA

# **B3 팀**

- 팀명 : 비상 ( 현재는 실력이 비상이지만 곧 비상하겠습니다. )
- 팀장 : 이원채, 김민수
- 팀원 : 강기훈, 김경민, 현준호

## 프로젝트 이름 - [ **Stady 스테디** ]

Stay와 Study의 합성어로 자리에 머물러 공부를 한다는 의미이다.

## 프로젝트 목적

- 프로젝트 이름에서 나타나듯 사람이 책상에 머무르며 공부할때 항상 옆을 지키며 공부를 도와준다.

- 카메라 앞에 앉아 공부중인 사람을 인식하여 자동으로 공부 중 여부를 확인하여 로그를 남긴다.

- 서비스 이용자가 웹캠 앞에서 공부할 때 Stady는 사람을 인식하고 공부로그를 자동으로 기록한다. 이후 집중한 시간에 무엇을 했는지 메모로 남기고 피드백 할 수 있도록 도와준다. 뿐만 아니라 Stady 이용자간의 소통을 통해 이용자들의 커뮤니티를 만들고 궁극적으로 Stady 이용자들이 공부하는데 도움을 제공하는게 목적이다.

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
