# Stady Project 딥러닝

### 레퍼런스

---

[공작소](https://www.gongzakso.com/)

### 툴

---

[피그마](https://www.figma.com/file/kBCcltpdL2D6QG6kQV01cD/Untitled?node-id=0%3A1)

[ERD](https://www.erdcloud.com/d/BYxpMAdg9QcLRupjg)

### 기타

---

[잼보드](https://jamboard.google.com/d/1Bdh9nlqy0WqR_PLrCOJHXvcz_ZwfgXGMfQTYgqp4UXY/viewer?f=0)

[팀회고 잼보드](https://jamboard.google.com/d/1YwARzhHt1EIsbWT8DFY1Zb3etAGyrNoriYOINm-xkTw/viewer?ts=635255fc&f=3)

# **B3 팀**

- 팀명 : (주) 스테디
- 팀장 :이원채
- 팀원 : 강기훈, 현준호, 김민수, 김경민

## 프로젝트 이름 - [ **Stady (스테디)** ]

stay와 study의 합성어로 자리에 머물러 공부를 한다는 의미로, 자리에 앉아 공부하는 사람을 인식해 주는 프로그램의 목적에 맞게 이름을 지었다.

## 이번 프로젝트 목적

- 팀원들 DRF를 다루고 프론트와 통신 가능하고 표현할 수 있는 것
- 프로젝트 배포에 대한 이해

## 팀 약속

- 오전 9시 30분 팀 회의
- 오후 7시 각자의 공부내용, 코드 발표
- 마감기한 잘 지키기!
- 이슈 2일에 하나씩 등록하기 (권장 사항) - 메모장으로 사용하기

## 팀 역할

기훈 - 커뮤니티 게시판 구현

원채 - TODO 리스트 기능 구현

민수 - 커뮤니티 백엔드, 프론트엔트

준호 - 딥러닝(게시글을 통해 감정 분석)

경민 - 스터디 전용 서비스(백, 프론트), 에러 보수

[개발 일정](https://www.notion.so/bfc4f0a3b08a4061a52b6dd0d9bedb8d)

## 깃 브랜치

feature/community : 민수, 원채, 기훈

feature/group : 경민

feature/todo : 원채

feature/diary: 준호

## 기능

- 스터디 그룹을 모집 & 참여할 수 있는 서비스 추가
- 로그 혹은 좋아요를 이용한 스터디 추천 서비스 추가
- 커뮤니티

## 와이어 프레임
<img width="832" alt="Untitled" src="https://user-images.githubusercontent.com/113074274/204202089-44f0a772-2359-45f4-b603-f8ab52764e26.png">
<img width="400" alt="Untitled 1" src="https://user-images.githubusercontent.com/113074274/204202131-2b88987e-e4fc-4e13-a46a-e1c02fd735dd.png">
<img width="413" alt="Untitled 2" src="https://user-images.githubusercontent.com/113074274/204202135-574d70b6-9876-4cba-a39b-571e616f950d.png">
<img width="345" alt="Untitled 3" src="https://user-images.githubusercontent.com/113074274/204202143-9613c51e-b030-4785-8d31-8b8dff4d5d8b.png">
<img width="449" alt="Untitled 4" src="https://user-images.githubusercontent.com/113074274/204202203-65bd0e1b-2f11-4b16-a3b4-d5b1aaabcffc.png">
<img width="360" alt="Untitled 5" src="https://user-images.githubusercontent.com/113074274/204202208-8e4b8ab2-e49d-48e4-97e9-6e49b3c042a4.png">
<img width="361" alt="Untitled 6" src="https://user-images.githubusercontent.com/113074274/204202221-4316aa99-0885-450f-8e2f-d0ac1c2e4a05.png">


## ERD
![Untitled 7](https://user-images.githubusercontent.com/113074274/204202291-3358238a-4af8-471e-8229-5867f7b27d46.png)

## User API
| 기능 | method | url | request | response | 비고 |  |
| --- | --- | --- | --- | --- | --- | --- |
| 회원가입 | GET | /user/join/ |  |  |  |  |
|  | POST | /user/join/ | {</br>’email’ : email,</br>’username’ : username,</br>’password’ : password,</br>’password2’ : password2,</br>} |  |  |  |
| 로그인 | POST | /api/token/ | {</br>’email’ : email ,</br>’password’ : password</br>} | {</br>’refresh’ : refresh,</br>’access’ : access</br>} |  |  |
|  |  |  |  |  |  |  |
| 로그아웃 | GET | /user/logout/ |  |  |  |  |
|  |  |  |  |  |  |  |
| 정보수정 | PUT | /user/update/ | {</br>’email’ : email,</br>’username’ : username,</br>} |  |  |  |
|  |  |  |  |  |  |  |
| 회원탈퇴 | GET | /user/delete/ |  |  |  |  |
## 공부 로그 Service API
| 기능 | Method | URL | Request | Response | 비고 |
| --- | --- | --- | --- | --- | --- |
| 공부 시작 | GET | /study/ | {</br>’type’ : ‘start’</br>} | - |  |
| 공부 종료 | GET | /study/ | {</br>’type’ : ‘finish’</br>} | - |  |
| 공부 참여 체크 | POST | /study/ | {</br>’img’ : img</br>} | - |  |
| 공부 메모 | PUT | /study/ | {</br>’log_id’ : log_id ,</br>’memo’ : memo</br>} |  |  |
| 공부 로그 에러 처리 | DELETE | /study/ | - | {</br>’study_log_list’:study_log_list</br>} |  |
|  |  |  |  |  |  |
| 공부 로그 가져오기 | GET | /study/log/ | {</br>’day’ : day</br>} | {</br>’study_log_list’:study_log_list</br>} | 특정 날짜의 로그를 보내주는 api |
|  |  |  |  |  |  |
| 일기 작성 | GET | /study/diary/ |  |  |  |
|  | POST |  | {</br>’title’:title,</br>’content’:content,</br>’feeling’:feeling</br>} |  |  |
## 스터디 서비스 API
| 기능 | Method | URL | Request | Response | 비고 |
| --- | --- | --- | --- | --- | --- |
| 스터디 메인 | GET | /studies/ |  | {</br>”studies” : studies</br>} |  |
| 스터디 모집글 생성 | POST | /studies/ | {</br>”title” : title,</br>”content” : content,</br>”headcount” : headcount,</br>”is_online” : is_online,</br>”is_penalty” : is_penalty,</br>”days” : days,</br>”penalty” : penalty,</br>”tags” : tags</br>} |  |  |
| 스터디 보기 | GET | /studies/<int:study_id>/ |  | {</br>”title” : title,</br>”is_author”: is_author,</br>”is_student”:is_student,</br>”is_like” : is_like,</br>”sended”: sended,</br>”content” : content,</br>”headcount” : headcount,</br>”is_online” : is_online,</br>”is_penalty” : is_penalty,</br>”days” : days,</br>”penalty” : penalty,</br>”tags” : tags</br>} |  || 스터디 모집글 수정 | PUT | /studies/<int:study_id>/ | {</br>”title” : title,</br>”content” : content,</br>”headcount” : headcount,</br>”is_online” : is_online,</br>”is_penalty” : is_penalty,</br>”days” : days,</br>”penalty” : penalty,</br>”tags” : tags</br>} |  |  |
| 스터디 모집글 삭제 | DELETE | /studies/<int:study_id>/ |  |  |  |
|  |  |  |  |  |  |
| 스터디 즐겨찾기 | POST | /studies/<int:study_id>/like/ |  |  |  |
|  |  |  |  |  |  |
| 스터디 신청 | GET | /studies/<int:study_id>/propose/ |  |  |  |
|  |  |  |  |  |  |
| 스터디 승낙 | POST | /studies/<int:study_id>/accept/<int:user_id> |  |  |  |
|  |  |  |  |  |  |
| 회원 프로필 - 공부로그 | GET | /profile/<int:user_id>/ |  |  |  |
|  | POST | /profile/<int:user_id>/ |  |  |  |
| 회원 프로필 - 스터디 | GET | /profile/<int:user_id>/study/ |  |  |  |
|  | POST | /profile/<int:user_id>/study/ |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
| 스터디원 전용 페이지 | GET | /studies/<int:study_id>/private/ | {</br>”community-type” : “info”,</br>} | {</br>”students”: students,</br>”study_info” : study_info,</br>”week_penalty”:week_penalty,</br>”total_penalty”:total_penalty</br>} |  |
| 스터디원 전용 게시판 | GET | /studies/<int:study_id>/private/ | - | {</br>”post_list” : post_list,</br>”page_cnt”:page_cnt,</br>”cur_page”: cur_page</br>} |  |
| 스터디원 전용 게시글 작성 | POST | /studies/<int:study_id>/private/ | {</br>”title” : title,</br>”content”: content,</br>”image”: image</br>} |  |  |
| 스터디원 전용 게시글 보기 수정 삭제 | PUT DELETE | /studies/<int:study_id>/private/<int:post_id>/ | {</br>”title” : title,</br>”content”: content,</br>”image”: image</br>} |  |  |
| 스터디원 전용 댓글 | POST | /studies/<int:study_id>/private/<int:post_id>/comment | {</br>”content” : content</br>} |  |  |
| 스터디원 전용 댓글 수정 삭제 | PUT DELETE | /studies/<int:study_id>/private/<int:post_id>/comment/<int:comment_id>/ | {</br>”content” : content</br>} |  |  |

| 기능 | method | url | request | response | 비고 |
| --- | --- | --- | --- | --- | --- |
| 게시글 리스트 | GET | /community/ | {</br>’category’ : category} | {</br>”post_list” : post_list</br>} | 조회수, 조회수 탑 |
| 게시글 작성 | POST | /community/ | {</br>’title : title’,</br>’content’:’content’,</br>’category’:’category’,</br>’img’:’img’</br>} |  | url 수정가능 |
|  |  |  |  |  |  |
| 게시글 디테일 | GET | /community/<int:post_id>/ |  | {</br>”title” : title,</br>”content” : content,</br>”image” : image,</br>”comment_list” : comment_list</br>} |  |
| 게시글 수정 | PUT | /community/<int:post_id>/ | {</br>’title : title’,</br>’content’:’content’,</br>’img’:’img’</br>} |  |  |
| 게시글 삭제 | DELETE | /community/<int:post_id>/ |  |  |  |
|  |  |  |  |  |  |
| 게시글 좋아요  | POST | /community/<int:post_id>/like/ | - | 200OK |  |
|  |  |  |  |  |  |
| 댓글 작성 | POST | /community/<int:post_id>/comment/ | {</br>”content” : content</br>} |  |  |
| 댓글 수정 | PUT | /community/<int:post_id>/comment/<int:comment_id>/ | {</br>”content” : content</br>} |  |  |
| 댓글 삭제 | DELETE | /community/<int:post_id>/comment/<int:comment_id>/ |  |  |  |
| 댓글 좋아요 | POST | /community/comment/<int:comment_id>/like/ | - |  |  |
|  |  |  |  |  |  |
| 검색 | GET | /community/search?= | {search:value} |  |  |

| 기능 | method | url | request | response | 비고 |
| --- | --- | --- | --- | --- | --- |
| 해야할일 작성 | POST | /todo/ | {  ”content” : content  } |  |  |
| 해야할일 목록 | GET | /todo/ |  |  |  |
| 해야할일 수정 | PUT | /todo/<int:todo_id>/ | {  ”content” : content  } |  |  |
| 해야할일 삭제 | DELETE | /todo/<int:todo_id>/ |  |  |  |
