# Instagram Feed Database Copy

## ERD 설계

![image](https://user-images.githubusercontent.com/43658658/132510879-06e0f7e9-c373-4580-9941-f3c2b9f5d135.png)

테이블은 크게 4개로 생각해 볼 수 있습니다.

1. User : 인스타의 유저에 관한 정보가 담기는 테이블입니다.
2. Feed : 피드에 들어갈 컨텐츠 정보가 담기는 테이블입니다.
3. clickLike : '좋아요'를 누른 회원의 정보가 담기는 테이블입니다.
4. Reply : 댓글과 관련한 정보가 담기는 테이블입니다.

타임라인에 있는 많은 피드들 중 하나의 피드를 클릭했을 때 그 피드에 대한 정보를 출력하는 SQL문을 작성하겠습니다.

``` mysql
-- 피드 유저, 피드 이미지, 피드 내용, 피드 올린 시각
select userID, imageUrl as feedImage, content,
    case
        when timestampdiff(second, createdAt, current_timestamp) <= 59
        then '방금 전'
        when timestampdiff(minute, createdAt, current_timestamp) <= 59
        then concat(timestampdiff(minute, createdAt, current_timestamp),'분 전')
        when timestampdiff(hour, createdAt, current_timestamp) <= 23
        then concat(timestampdiff(hour, createdAt, current_timestamp), '시간 전')
        else date_format(createdAt, '%m월 %d일')
    end as createdAtFeed
from Feed
where userID='bllumusic';
```

![image](https://user-images.githubusercontent.com/43658658/132536182-76989683-53cf-418d-a12f-7c6181846dbc.png)

``` mysql
-- feed별 좋아요 개수
select feedNo, count(feedNo) as clickLikeCnt
from clickLike group by feedNo;
```

![image](https://user-images.githubusercontent.com/43658658/132538353-2d8e02ab-a397-40bb-9e93-b7f0957df4ab.png)

``` mysql
-- 좋아요 개수가 추가된 버전
select Feed.userID, imageUrl as feedImage, clickLikeCnt, content,
    case
        when timestampdiff(second, Feed.createdAt, current_timestamp) <= 59
        then '방금 전'
        when timestampdiff(minute, Feed.createdAt, current_timestamp) <= 59
        then concat(timestampdiff(minute, Feed.createdAt, current_timestamp),'분 전')
        when timestampdiff(hour, Feed.createdAt, current_timestamp) <= 23
        then concat(timestampdiff(hour, Feed.createdAt, current_timestamp), '시간 전')
        else date_format(Feed.createdAt, '%m월 %d일')
    end as createdAtFeed
from Feed
inner join (select feedNo, count(feedNo) as clickLikeCnt
from clickLike group by feedNo) as clickLike
on clickLike.feedNo = Feed.feedNo
where Feed.userID='bllumusic';
```

![image](https://user-images.githubusercontent.com/43658658/132538723-d8b3c728-585c-4c43-934b-477dce5c218e.png)

