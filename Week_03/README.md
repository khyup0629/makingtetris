# Week 3.

- ERD 작성
- AWS RDS (DB) 생성
- Datagrip 에 테이블 작성
- Quary문 실습

## ERD 작성

카카오톡의 채팅 목록 화면을 `ERD 설계`해봅시다.

- [카카오톡 채팅 목록 화면 ERD 설계 가이드 메뉴얼](https://yusang.tistory.com/42?category=835611)
- [Ubuntu MySQL 외부에서 접속하기](https://luminitworld.tistory.com/82) : Datagrip을 통해 접속하는 방법, 데이터베이스 권한 설정 명령어 복습.

`AQueryTool`에서 ERD 기본 정보 설정

![image](https://user-images.githubusercontent.com/43658658/132428155-242e45df-95b6-4d50-8411-69a27c4549ce.png)

톱니바퀴 모양의 `옵션 설정` 버튼을 클릭하여 테이블에 보여지는 항목을 선택할 수 있습니다.

![image](https://user-images.githubusercontent.com/43658658/132428555-8d7af084-537c-4643-94b6-89c98a99de1e.png)

아래와 같이 테이블을 작성합니다.

![image](https://user-images.githubusercontent.com/43658658/132438490-ddcf8a90-3a3d-40ef-b70e-f8b859cec695.png)

User : 총 어떤 유저들이 있는지를 나타냅니다.   
Member : 유저가 어떤 대화방에 속해 있는지를 나타냅니다.   
Room : 어떤 대화방들이 있는지를 나타냅니다.   
Chat : 각 대화방에서 나눴던 대화들이 기록되는 테이블입니다.   
Friend : userID와 친구인 다른 유저들을 1대1 대응으로 기록합니다.   

- isDeleted, CHAR(1), N : 유저 데이터 지우기, N은 탈퇴를 하지 않았다는 뜻입니다.
- createdAt, TIMESTAMP, CURRENT_TIMESTAMP : 데이터가 생성될 때 시간을 자동으로 기록합니다.
- updatedAt, TIMESTAMP, current_timestamp on update current_timestamp : 데이터가 수정되었을 때, 시간을 기록합니다.
- Status : 휴면, 비활성, 차단 유저 상태를 나타냅니다(위의 테이블에는 없는 속성입니다).
- VARCHAR(45) : 길이가 45 제한인 String
- TEXT : 길이가 긴 String
- Null : 비어있어도 되는 항목인지.

## Datagrip에 데이터 입력 후 Query문 실습

> <h3>Datagrip에 데이터 입력</h3>

- [ERD 설계 후 Datagrip으로 데이터 관리하기](https://yusang.tistory.com/42?category=835611)

먼저 생성한 데이터베이스의 콘솔을 열고 `AQueryTool`에서 작성했던 테이블을 SQL문의 `.txt`파일로 저장한 후 텍스트를 복사, 붙여넣기 후 실행합니다.

생성된 테이블 속에 데이터를 입력합니다.   
카카오톡 채팅 목록 화면에 띄워지는 여러 정보를 바탕으로 각 테이블에 맞는 데이터를 작성해줍니다.

만약 테이블 칼럼의 Type을 수정해야한다면, 좌측 탭의 해당 테이블에서 우클릭 -> Modify Table

Chat : 각 대화방에서 나눴던 대화들이 기록되는 테이블입니다.   
![image](https://user-images.githubusercontent.com/43658658/132441336-14f663a7-9b49-41d8-8203-35fb221ea75b.png)

Friend : userID와 친구인 다른 유저들을 1대1 대응으로 기록합니다.   
![image](https://user-images.githubusercontent.com/43658658/132441365-66f9da8d-8419-4cfb-b9ce-3855f239ec21.png)

Member : 유저가 어떤 대화방에 속해 있는지를 나타냅니다.   
![image](https://user-images.githubusercontent.com/43658658/132441375-93842bf3-436e-45bf-b924-07d20c3f22af.png)

Room : 어떤 대화방들이 있는지를 나타냅니다.   
![image](https://user-images.githubusercontent.com/43658658/132442469-b23c5519-cda0-43db-8c68-841da90a94b1.png)

User : 총 어떤 유저들이 있는지를 나타냅니다.   
![image](https://user-images.githubusercontent.com/43658658/132441400-60d6c409-300e-4c89-b0fc-06857dbe55f1.png)

데이터를 모두 `작성/수정`한 뒤엔 `[Ctrl]+[Enter]`를 이용해 꼭 `Submit`을 해주어야합니다.

> <h3>Query문 실습</h3>

``` mysql
select * from Member;
```

![image](https://user-images.githubusercontent.com/43658658/132441799-667e586c-62a4-41ee-a804-2b24ec9bf7b5.png)

``` mysql
select * from Chat where userID='khyup0629';
```

![image](https://user-images.githubusercontent.com/43658658/132442050-21be1852-e023-4c02-9039-1c804dc58a6a.png)

``` mysql
// Room 테이블의 데이터 중 roomNo가, khyup0629인 유저의 Member 테이블의 roomNo 데이터와 일치하는 데이터를 출력합니다.
select * from Room where roomNo in (select roomNo from Member where userID='khyup0629');
```

![image](https://user-images.githubusercontent.com/43658658/132442343-4c6cf77f-8034-43e1-8d6b-e3e2a74c0b48.png)

``` mysql
// from 'A' inner join 'B' on 'Criteria` : 'A'와 'B'를 'Criteria'를 기준으로 합칩니다.
// 중복되는 칼럼이 있을 경우 `테이블.칼럼`의 형식으로 적어줍니다.
select Room.roomNo, title, imageUrl, Room.createdAt 
from Member inner join Room on Room.roomNo = Member.roomNo
where userID = 'khyup0629';
```

![image](https://user-images.githubusercontent.com/43658658/132444293-21797f5a-38d1-4942-a9a8-e8feb10ad6ee.png)

``` mysql
// as를 이용해 칼럼의 출력되는 이름을 바꿀 수 있습니다.
select Room.roomNo, title as roomName, imageUrl as roomImageUrl, Room.createdAt
from Member inner join Room on Room.roomNo = Member.roomNo
where userID = 'khyup0629';
```

![image](https://user-images.githubusercontent.com/43658658/132444439-46d5b60c-5f9d-4f9e-943d-f14dd0a9600e.png)

``` mysql
// Chat 테이블의 roomNo별로 `no가 가장 큰` roomNo, no를 출력합니다.
select roomNo, max(no) as currentMessageNo from Chat group by roomNo;
```

![image](https://user-images.githubusercontent.com/43658658/132444709-3dd11a5a-2af6-4874-8f00-7cb6e7eb27b0.png)

``` mysql
// inner join ( ~ ) 'A' : 괄호 내의 칼럼들을 'A'라는 테이블로 묶습니다.
select * 
from Chat
inner join (select roomNo, max(no) as currentMessageNo 
from Chat group by roomNo) currentMessage;
```

![image](https://user-images.githubusercontent.com/43658658/132447812-c98f9bb0-0902-4db7-a537-c105838833fa.png)

``` mysql
// currentMessageNo와 no가 같은 데이터를 추려냅니다.
select Chat.roomNo, contents as lastMessage,
       type as lastMessageType, createdAt as lastMessageTimeStamp
from Chat
inner join (select roomNo, max(no) as currentMessageNo 
from Chat group by roomNo) currentMessage
where currentMessageNo = no;
```

![image](https://user-images.githubusercontent.com/43658658/132448793-65497d88-c006-4c86-8c85-fb04c48b9892.png)

> <h3>카카오톡 채팅 목록 화면 데이터만 뽑아내기</h3>

![image](https://user-images.githubusercontent.com/43658658/132444992-4065426d-1c34-4222-8e95-2dfa868cb171.png)

카카오톡 채팅 목록 화면에는 전체 테이블 중 `4개`의 칼럼이 나타나는 것을 볼 수 있습니다.   
`채팅방 이미지, 채팅방 이름, 채팅방 마지막 메세지 내용, 채팅방 마지막 메세지 시간`   

여기서 구분을 위해 `채팅방 번호, 채팅방 메세지 타입`을 추가해 총 `6개`의 칼럼으루 구성해보겠습니다.
`채팅방 번호, 채팅방 이미지, 채팅방 이름, 채팅방 마지막 메세지 내용, 채팅 메세지 타입, 채팅방 마지막 메세지 시간,`   

![image](https://user-images.githubusercontent.com/43658658/132444761-4fc9b120-cc78-4704-843f-eb7299943054.png)

6개의 칼럼은 현재 '나'인 `khyup0629`가 속해있는 톡방만 화면에 띄워질 것입니다.   
따라서, 앞서 작성한 두 가지의 SQL문을 합쳐서 `한방쿼리`로 작성해줍니다.   

``` mysql
// khyup0629가 속해있는 톡방만 화면에 띄웁니다.
select Room.roomNo, ImageUrl as roomImageUrl, title as roomName,
       lastMessage, lastMessageType, lastMessageTimeStamp
from Member inner join Room on Room.roomNo = Member.roomNo
where userID = 'khyup0629';
// + 톡방 별로 가장 최근 데이터를 뽑아냅니다.
select Chat.roomNo, contents as lastMessage,
       type as lastMessageType, createdAt as lastMessageTimeStamp
from Chat
inner join (select roomNo, max(no) as currentMessageNo 
from Chat group by roomNo) currentMessage
where currentMessageNo = no;
```

``` mysql
// 합쳐진 SQL문입니다.
select Room.roomNo, ImageUrl as roomImageUrl, title as roomName,
       lastMessage, lastMessageType, lastMessageTimeStamp
from Member
inner join Room
on Room.roomNo = Member.roomNo
inner join (select Chat.roomNo, contents as lastMessage,
       type as lastMessageType, createdAt as lastMessageTimeStamp
from Chat
inner join (select roomNo, max(no) as currentMessageNo
from Chat group by roomNo) currentMessage
where currentMessageNo = no) lastChatMessage
on lastChatMessage.roomNo = Member.roomNo
where userID = 'khyup0629';
```

![image](https://user-images.githubusercontent.com/43658658/132450456-51402c7c-bd45-49f3-8aad-fef20cdc13b6.png)

마지막으로, 가장 마지막으로 보낸 메세지의 시간(`lastMessageTimeStamp`)을 살펴봅시다.   
카카오톡의 시간 표시 기능은 현재 시간(current_timestamp)과 비교해 마지막으로 보낸 메세지의 시간(`lastMessageTimeStamp`)의   
연도(year)가 다르면 `2020-09-08`의 형식으로 나타내고,
월(month), 일(date)이 다르면 `m월 d일`로 나타내고, 같은 날인 경우 `오전/오후 hh:mm`으로 나타냅니다.   
그래서 이중 `case when/then`문을 사용하여 이를 구현해봅시다.   
(구글링을 통해 키워드 `mysql 날짜 형식`, `mysql 연도 추출`, `mysql case when`로 검색해서 공부합니다)

``` mysql
select Room.roomNo, ImageUrl as roomImageUrl, title as roomName,
    lastMessage, lastMessageType,
        case
            when year(lastMessageTimeStamp) != year(current_timestamp)
            then date_format(lastMessageTimeStamp, '%Y-%m-%d')
            when date_format(lastMessageTimeStamp, '%y%m%d') != date_format(current_timestamp, '%y%m%d')
            then date_format(lastMessageTimeStamp, '%m월 %d일')
            else case when date_format(lastMessageTimeStamp, '%p') = 'AM'
                then date_format(lastMessageTimeStamp, '오전 %h:%m')
                else date_format(lastMessageTimeStamp, '오후 %h:%m')
                end
        end as lastMessageTimeStamp
from Member
inner join Room
on Room.roomNo = Member.roomNo
inner join (select Chat.roomNo, contents as lastMessage,
    type as lastMessageType, createdAt as lastMessageTimeStamp
from Chat
inner join (select roomNo, max(no) as currentMessageNo
from Chat group by roomNo) currentMessage
where currentMessageNo = no) lastChatMessage
on lastChatMessage.roomNo = Member.roomNo
where userID = 'khyup0629';
```

![image](https://user-images.githubusercontent.com/43658658/132496229-727c7e54-a40a-4a92-bfac-4c8f2dd77b2d.png)
