# Stady Project (2)

### 레퍼런스

---

[공작소](https://www.gongzakso.com/)

### 툴

---

[피그마](https://www.figma.com/file/kBCcltpdL2D6QG6kQV01cD/Untitled?node-id=0%3A1)

[ERD](https://www.erdcloud.com/d/BYxpMAdg9QcLRupjg)


# **B3 팀**

- 팀명 : (주) 스테디
- 팀장 :김민수, 김경민
- 팀원 : 강기훈, 이원채,  현준호

## 프로젝트 이름 - [ **Stady (스테디) ]**

stay와 study의 합성어로 자리에 머물러 공부를 한다는 의미로, 자리에 앉아 공부하는 사람을 인식해 주는 프로그램의 목적에 맞게 이름을 지었다.

### 목적

- 카메라 앞에 앉아 공부중인 사람을 인식하여 자동으로 공부 중 여부를 확인하여 로그를 남기도록 한다.

서비스를 이용하는 사용자가 공부에 집중 할 수 있도록 공부 집중 시간을 기록하고 집중한 시간에 무엇을 하였는지 메모로 남길 수 있는 서비스를 구현하고 자 프로젝트를 계획했다.

- 비슷한 목적을 가진 사람들에게 공부를 도모할 수 있도록 스터디 그룹을 만들고 참여할 수 있는 서비스를 계획하였다.

## 이번 DRF 프로젝트 목적

- 기존 기능의 FBV에서 CBV로 바꾸는 것.
- 추가 기능(스터디 그룹) 또한 CBV로 만드는 것.
- 태그 혹은 좋아요를 기반으로 추천 시스템을 구축하는 것

## 팀 약속

- 마감을 잘 지키자!
- 주말에도 일하자!(안돼요ㅠㅠ)
- 잘때자고 밥먹을때 밥 먹자!
- 깃허브 컨벤션 확인
- 모델 변경 시 팀원들에게 알리기
- 각자 쓴 코드 리뷰하기 ( 7 or 5 )
- 깃허브를 적극 활용하기

## 팀 역할

기훈 - 스터디 그룹 생성, 수정, 삭제

원채 - 프로필 ( 공부로그, 스터디 그룹들)

민수 - 스터디 그룹 메인( 최신, 검색)

준호 - 스터디 그룹 디테일 ( 주최자-수락거절, 수정 삭제 , 참여자- 신청취소)

경민 - 회원관련, 로그, 관심분야, 태그, 프론트, 에러 처리

## 기능

- 스터디 그룹을 모집 & 참여할 수 있는 서비스 추가
- 로그 혹은 좋아요를 이용한 스터디 추천 서비스 추가

## 와이어 프레임
![Untitled](https://user-images.githubusercontent.com/113074274/200484765-d17c107f-3a71-46c9-84fa-37ff00b26352.png)

![Untitled 1](https://user-images.githubusercontent.com/113074274/200484784-5f1183bf-774a-41e7-b887-0f4dedee563d.png)

![Untitled 2](https://user-images.githubusercontent.com/113074274/200484789-db77a8c4-746e-4e3b-8de0-fdff05743588.png)

![Untitled 3](https://user-images.githubusercontent.com/113074274/200484791-cbdaa50b-e45c-41ad-bf44-4e5b1f464399.png)

![Untitled 4](https://user-images.githubusercontent.com/113074274/200484794-94377e22-8bcb-4ce3-a844-66bbfef75769.png)

![Untitled 5](https://user-images.githubusercontent.com/113074274/200484795-96eadaf2-6c30-40d8-a2ad-97359bd217ac.png)


## ERD

![Untitled 6](https://user-images.githubusercontent.com/113074274/200484827-29ec0bf6-cc2c-4fea-bdb2-d90489b2199d.png)

## User API

| 기능 | method | url | request | response | 비고 |  |
| --- | --- | --- | --- | --- | --- | --- |
| 회원가입 | GET | /user/join |  |  |  |  |
|  | POST | /user/join |  |  |  |  |
| 로그인 | POST | /api/token |  |  |  |  |
|  |  |  |  |  |  |  |
| 로그아웃 | GET | /user/logout |  |  |  |  |
|  |  |  |  |  |  |  |
| 정보수정 | PUT | /user/update |  |  |  |  |
|  |  |  |  |  |  |  |
| 비밀번호변경 | GET | /user/change_password |  |  |  |  |
| 비밀번호변경 | POST | /user/change_password |  |  |  |  |
| 이메일 인증 비밀번호 리셋 | GET | /user/password_reset |  |  |  |  |
|  | POST | /user/password_reset |  |  |  |  |
| 이메일 인증 비밀번호 리셋 완료알림 | GET | /user/reset_password_done |  | user/reset_password_done.html |  |  |
|  | POST | /user/reset_password_done |  | user/login.html |  |  |
| 이메일 인증 비밀번호 리셋 결정 | GET | /user/reset_password_confirm |  | /user/reset_password_confirm.html |  |  |
|  | POST | /user/reset_password_confirm |  | /user/login/html |  |  |
| 회원탈퇴 | GET | /user/delete |  | user/delete.html |  |  |
|  | POST | /user/delete |  | user/login.html |  |  |

## Service API

| 기능 | Method | URL | Request | Response | 비고 |
| --- | --- | --- | --- | --- | --- |
| 회원 프로필 | GET | /profile/<pk:user_id> |  |  |  |
|  |  |  |  |  |  |
| 공부 시작 | GET | /study/ |  | - |  |
| 공부 종료 | GET | /study/ |  | - |  |
| 공부 참여 체크 | POST | /study/ | | - |  |
| 공부 메모 | PUT | /study/ |  |  |  |
| 공부 로그 에러 처리 | DELETE | /study/ | - | |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
| 공부 로그 가져오기 | GET | /study/log |  |  | 특정 날짜의 로그를 보내주는 api |

## 스터디 서비스 API

| 기능 | Method | URL | Request | Response | 비고 |  |
| --- | --- | --- | --- | --- | --- | --- |
| 회원 프로필 | GET | /profile/<pk:user_id>/ |  |  |  |  |
|  |  |  |  |  |  |  |
| 스터디 메인 | GET | /studies/ |  |  |  |  |
| 스터디 모집글 생성 | POST | /studies/ |  |  |  |  |
| 스터디 보기 | GET | /studies/<int:study_id>/ |  |  |  |  |
| 스터디 모집글 수정 | PUT | /studies/<int:study_id>/ |  |  |  |  |
| 스터디 모집글 삭제 | DELETE | /studies/<int:study_id>/ |  |  |  |  |
|  |  |  |  |  |  |  |
| 스터디 즐겨찾기 | POST | /studies/<int:study_id>/like/ |  |  |  |  |
|  |  |  |  |  |  |  |
| 스터디 신청 | GET POST | /studies/<int:study_id>/propose/ |  |  |  |  |
|  |  |  |  |  |  |  |
| 스터디 승낙 | POST | /studies/<int:study_id>/accept/<int:user_id> |  |  |  |  |
|  |  |  |  |  |  |  |
| 회원 프로필 - 공부로그 | GET | /profile/<int:user_id> |  |  |  |  |
|  | POST | /profile/<int:user_id> |  |  |  |  |
| 회원 프로필 - 스터디 | GET | /profile/<int:user_id>/study/ |  |  |  |  |
|  | POST | /profile/<int:user_id>/study/ |  |  |  |  |
|  |  |  |  |  |  |  |
