![스테디배너](https://user-images.githubusercontent.com/113074274/204524489-54a8e293-0e50-471e-889b-6322837f7d73.png)
# Stady
- stay와 study의 합성어이며 자리에 머물러 공부를 한다는 의미로 공부하는 이들을 위한 서비스.

## :alien: **Our Team**

- 팀명 : (주) 스테디
- 팀원 : 강기훈, 현준호, 김민수, 김경민, 이원채

## :art: **Stack**
Backend : <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/django rest framework-092E20?style=for-the-badge&logo=django&logoColor=white">
<br>

Frontend : <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white">
<img src="https://img.shields.io/badge/jquery-0769AD?style=for-the-badge&logo=jquery&logoColor=white">
<img src="https://img.shields.io/badge/ajax-0769AD?style=for-the-badge&logo=jquery&logoColor=white">
<img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">



<br>

## :sparkles:주요 기능

### 자동 공부 로그! <br>
> 시간은 내가 잴게.
<br>

![메인기능](https://user-images.githubusercontent.com/112795528/210121734-876d78cd-7504-45a6-b433-b370ad85954d.gif)

- 웹캠을 이용하여 주기적으로 사람이 인식되는지에 대한 여부로 실제 공부 시간을 측정하고 로그를 남깁니다.

### Log & Todo <br>
> 계획, 그리고 기록
<br>

![todo](https://user-images.githubusercontent.com/112795528/210121740-febcb10a-d06d-4d92-a5fc-9aca7a889b7a.gif) <br>

- Todo 리스트를 생성하여 오늘의 계획을 짤 수 있습니다.
- 자동 생성된 공부 로그에 어떤 것을 공부했는지 기록을 남길 수 있습니다.

### 스터디 생성 <br>
> 벌금 스터디라고 들어봤어?

![스터디 신청](https://user-images.githubusercontent.com/112795528/210121753-b254d210-d489-4ace-a01e-3b638e059d86.gif) <br>

- 하루 총 공부시간 or 출석 체크 시간을 기준으로 벌금 포인트를 걷을 수 있습니다.
- 물론 일반 스터디도 모집할 수 있습니다.

### 스터디 추천 <br>
> 이건 어때?

![추천](https://user-images.githubusercontent.com/78214692/210173205-34121620-8f1a-4e21-9bdd-d34a2a368098.gif)

- 스터디 태그와 유저의 방문 횟수로 회원간 코사인 유사도를 구해서 추천해 줍니다.

### 스터디 
![스터디 신청,관리](https://user-images.githubusercontent.com/112795528/210121758-6f941b88-8b38-49e1-9d65-270f4e1794ed.gif) <br>
- 신청, 수락/거절
  - 원하는 스터디를 신청/신청취소/탈퇴 합니다.
  - 관리자는 수락/거절/추방이 가능합니다.

- 스터디원 전용 게시판
  - 회원들의 정보를 볼 수 있습니다.
  - 관리자는 회원 관리를 할 수 있습니다.
  - 게시글, 댓글, 좋아요 기능이 있습니다.

<details>
<summary><h3>:one:차(22.10.17~22.10.20) </h3></summary>
<div markdown ="1">

#### 회원가입, 로그인, 로그아웃

- SNS연동 로그인
- 이메일 인증

#### 정보 수정, 비밀번호 변경

#### :pencil2: 공부 로그 자동 기록

- 공부 로그 & 머신러닝 연동
- 날짜별 공부 로그 기록 보기
</div>
</details>

<details>
<summary><h3>:two:차(22.11.02~22.11.08) </h3></summary>
<div markdown ="1">

#### 프론트앤드 & 백앤드 분리(DRF)

#### :closed_book: 스터디 그룹을 모집 & 참여할 수 있는 서비스 추가

- 스터디 그룹 생성, 수정, 삭제
- 스터디 그룹 메인( 최신, 검색)
- 스터디 그룹 디테일 ( 주최자-수락거절, 수정 삭제 , 참여자- 신청취소)
- 스터드 그룹 즐겨 찾기 기능 추가

#### 개인 프로필 페이지 추가( 공부로그, 스터디 그룹들)

- 신청한 그룹 리스트 보기, 즐겨 찾기 리스트 보기

#### :ballot_box_with_check:스터디 추천 서비스 추가

- 태그를 통한 스터디 그룹 추천 시스템
</div>
</details>

<details>
<summary><h3>:three:차(22.11.22~22.11.28) </h3></summary>
<div markdown ="1">

#### :lips: 커뮤니티

- 익명 게시판(랜덤 닉네임 생성) & 자유 게시판
- 게시글 생성, 수정, 삭제
- 댓글 생성, 수정, 삭제

#### 스터디 그룹

- 스터디 그룹 전용 페이지
- 모집 정보 수정, 삭제
- 게시글 작성, 수정, 삭제

#### :moneybag: 벌금 제도

#### :white_check_mark: Todo 리스트 추가

#### Error 보수

</div>
</details>

## 와이어 프레임([피그마](https://www.figma.com/file/4euWhIaup0RZ53UDJXCTk3/Untitled?t=SFakNXjLpgUrg56C-0))
![image](https://user-images.githubusercontent.com/113074274/204526136-093a5077-2073-4562-a364-5b008fc636ef.png)

## ERD([Erdcloud](https://www.erdcloud.com/d/BYxpMAdg9QcLRupjg))
![스크린샷 2023-01-01 오후 10 56 55](https://user-images.githubusercontent.com/78214692/210173115-b0f1f620-a786-4fb7-9440-fbe57db366d1.png)

## User API

![image_1](https://user-images.githubusercontent.com/113074274/204511286-4206c1da-e351-42d2-9e85-54a533f581ed.png)

## 공부 로그 Service API

![image_2](https://user-images.githubusercontent.com/113074274/204511296-e1571494-13dc-4b36-8bbc-7b3ec8244a48.png)

## 스터디 서비스 API

![image_3](https://user-images.githubusercontent.com/113074274/204511317-0afcb819-0088-4ae2-b5cb-56284c7a63cb.png)
![image_4](https://user-images.githubusercontent.com/113074274/204511358-59245fc9-fa23-4c1d-825f-aed88b38e3a9.png)

## ETC

[잼보드](https://jamboard.google.com/d/1Bdh9nlqy0WqR_PLrCOJHXvcz_ZwfgXGMfQTYgqp4UXY/viewer?f=0)

[팀회고 잼보드](https://jamboard.google.com/d/1YwARzhHt1EIsbWT8DFY1Zb3etAGyrNoriYOINm-xkTw/viewer?ts=635255fc&f=3)
