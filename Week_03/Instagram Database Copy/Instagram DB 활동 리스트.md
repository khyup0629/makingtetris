# 활동 리스트

![image](https://user-images.githubusercontent.com/43658658/133030941-f9fb1d1a-cc58-4ab0-bf62-d6d3f010a7ba.png)

> <h3>게시글 별 좋아요 현황</h3>

``` mysql
-- 블루뮤직 피드별 이미지 URL
select *
from FeedImageTable
where feedimageno in (select min(feedImageNo) from FeedImageTable group by feedImageFeedNo)
  and feedImageUserID = 'bllumusic';

-- 블루뮤직 피드별 동영상 URL
select *
from FeedVideoTable
where feedVideoNo in (select min(feedVideoNo) from FeedVideoTable group by feedvideoFeedNo)
  and feedvideoUserID = 'bllumusic';

-- 블루뮤직 피드별 이미지 + 동영상 번호
select *
from FeedImageTable
where feedimageno in
      (select min(feedImageNo) from FeedImageTable group by feedImageFeedNo)
  and feedImageUserID = 'bllumusic'
union all
select *
from FeedVideoTable
where feedVideoNo in
      (select min(feedVideoNo) from FeedVideoTable group by feedvideoFeedNo)
  and feedvideoUserID = 'bllumusic';

-- 블루뮤직의 피드별 제일 첫 번째로 올린 이미지 or 동영상 번호
select feedImageFeedNo, feedImageUrl as firstUrlPerFeed
from (select *
      from FeedImageTable
      where feedimageno in
            (select min(feedImageNo) from FeedImageTable group by feedImageFeedNo)
        and feedImageUserID = 'bllumusic'
      union all
      select *
      from FeedVideoTable
      where feedVideoNo in
            (select min(feedVideoNo) from FeedVideoTable group by feedvideoFeedNo)
        and feedvideoUserID = 'bllumusic') as contentUrlPerFeed
where feedImageNo in (select min(feedImageNo)
                      from (select *
                            from FeedImageTable
                            where feedimageno in
                                  (select min(feedImageNo) from FeedImageTable group by feedImageFeedNo)
                              and feedImageUserID = 'bllumusic'
                            union all
                            select *
                            from FeedVideoTable
                            where feedVideoNo in
                                  (select min(feedVideoNo) from FeedVideoTable group by feedvideoFeedNo)
                              and feedvideoUserID = 'bllumusic') as onlyOneUrlPerFeed
                      group by feedImageFeedNo);

-- 블루뮤직의 피드를 좋아요 누른 유저들
select *
from ClickLikeTable
where clickLikeFeedNo in (select feedNo
                          from FeedTable
                          where feedHost = 'bllumusic');

-- 블루뮤직의 피드별 가장 최근 좋아요 누른 번호
select clickLikeFeedNo, max(clickLikeNo) as lastClickLikeNo
from (select *
      from ClickLikeTable
      where clickLikeFeedNo in (select feedNo
                                from FeedTable
                                where feedHost = 'bllumusic')) as lastClickLikeTable
group by clickLikeFeedNo;

-- 좋아요 고유 번호와 대응되는 유저 ID와 좋아요 누른 시간
select clickLikeFeedNo,
       clickLikeNo,
       clickLikeUserID,
       case
           when timestampdiff(second, clickLikeCreatedAt, current_timestamp) < 60
               then concat(timestampdiff(second, clickLikeCreatedAt, current_timestamp), '초')
           when timestampdiff(minute, clickLikeCreatedAt, current_timestamp) < 60
               then concat(timestampdiff(minute, clickLikeCreatedAt, current_timestamp), '분')
           when timestampdiff(hour, clickLikeCreatedAt, current_timestamp) < 24
               then concat(timestampdiff(hour, clickLikeCreatedAt, current_timestamp), '시간')
           when timestampdiff(day, clickLikeCreatedAt, current_timestamp) < 7
               then concat(timestampdiff(day, clickLikeCreatedAt, current_timestamp), '일')
           else date_format(clickLikeCreatedAt, '%m월 %d일')
           end as lastFeedTimestamp
from ClickLikeTable
where clickLikeNo in (select max(clickLikeNo) as lastClickLikeNo
                      from (select *
                            from ClickLikeTable
                            where clickLikeFeedNo in (select feedNo
                                                      from FeedTable
                                                      where feedHost = 'bllumusic')) as lastClickLikeTable
                      group by clickLikeFeedNo)
order by clickLikeNo DESC;

-- 블루 뮤직의 피드별 좋아요 수
select clickLikeFeedNo, count(clickLikeNo) as lastClickLikeCnt
from (select *
      from ClickLikeTable
      where clickLikeFeedNo in (select feedNo
                                from FeedTable
                                where feedHost = 'bllumusic')) as lastClickLikeTable
group by clickLikeFeedNo;

-- 가장 최근 좋아요를 기준으로 내림차순 정렬하면서 블루 뮤직의 피드별 좋아요 현황
select lastClickLikeUserAndTimestamp.clickLikeFeedNo                                           as actClickLikeFeed,
       if(lastClickLikeCnt = 1, concat(clickLikeUserID, '님이 좋아합니다.'),
          concat(clickLikeUserID, ' 외 ', clickLikeCntByFeed.lastClickLikeCnt - 1, '명이 좋아합니다')) as actClickLikeUserCnt,
       actRecentClickLikeTime
from (select clickLikeFeedNo,
             clickLikeNo,
             clickLikeUserID,
             case
                 when timestampdiff(second, clickLikeCreatedAt, current_timestamp) < 60
                     then concat(timestampdiff(second, clickLikeCreatedAt, current_timestamp), '초')
                 when timestampdiff(minute, clickLikeCreatedAt, current_timestamp) < 60
                     then concat(timestampdiff(minute, clickLikeCreatedAt, current_timestamp), '분')
                 when timestampdiff(hour, clickLikeCreatedAt, current_timestamp) < 24
                     then concat(timestampdiff(hour, clickLikeCreatedAt, current_timestamp), '시간')
                 when timestampdiff(day, clickLikeCreatedAt, current_timestamp) < 7
                     then concat(timestampdiff(day, clickLikeCreatedAt, current_timestamp), '일')
                 else date_format(clickLikeCreatedAt, '%m월 %d일')
                 end as actRecentClickLikeTime
      from ClickLikeTable
      where clickLikeNo in (select max(clickLikeNo) as lastClickLikeNo
                            from (select *
                                  from ClickLikeTable
                                  where clickLikeFeedNo in (select feedNo
                                                            from FeedTable
                                                            where feedHost = 'bllumusic')) as lastClickLikeTable
                            group by clickLikeFeedNo)) as lastClickLikeUserAndTimestamp
         inner join
     (select clickLikeFeedNo, count(clickLikeNo) as lastClickLikeCnt
      from (select *
            from ClickLikeTable
            where clickLikeFeedNo in (select feedNo
                                      from FeedTable
                                      where feedHost = 'bllumusic')) as lastClickLikeTable
      group by clickLikeFeedNo) as clickLikeCntByFeed
     on clickLikeCntByFeed.clickLikeFeedNo = lastClickLikeUserAndTimestamp.clickLikeFeedNo
order by clickLikeNo DESC;

-- 유저 프로필 이미지, 피드 이미지가 추가된 좋아요 현황
select ProfileTable.profileImageUrl,
       if(lastClickLikeCnt = 1, concat(clickLikeUserID, '님이 회원님의 게시글을 좋아합니다.'),
          concat(clickLikeUserID, ' 외 ', clickLikeCntByFeed.lastClickLikeCnt - 1,
                 '명이 회원님의 게시글을 좋아합니다.')) as actClickLikeUserCnt,
       actRecentClickLikeTime,
       firstFeedUrlTable.firstUrlPerFeed as actClickLikeFeed
from (select clickLikeFeedNo,
             clickLikeNo,
             clickLikeUserID,
             case
                 when timestampdiff(second, clickLikeCreatedAt, current_timestamp) < 60
                     then concat(timestampdiff(second, clickLikeCreatedAt, current_timestamp), '초')
                 when timestampdiff(minute, clickLikeCreatedAt, current_timestamp) < 60
                     then concat(timestampdiff(minute, clickLikeCreatedAt, current_timestamp), '분')
                 when timestampdiff(hour, clickLikeCreatedAt, current_timestamp) < 24
                     then concat(timestampdiff(hour, clickLikeCreatedAt, current_timestamp), '시간')
                 when timestampdiff(day, clickLikeCreatedAt, current_timestamp) < 7
                     then concat(timestampdiff(day, clickLikeCreatedAt, current_timestamp), '일')
                 else date_format(clickLikeCreatedAt, '%m월 %d일')
                 end as actRecentClickLikeTime
      from ClickLikeTable
      where clickLikeNo in (select max(clickLikeNo) as lastClickLikeNo
                            from (select *
                                  from ClickLikeTable
                                  where clickLikeFeedNo in (select feedNo
                                                            from FeedTable
                                                            where feedHost = 'bllumusic')) as lastClickLikeTable
                            group by clickLikeFeedNo)) as lastClickLikeUserAndTimestamp
         inner join
     (select clickLikeFeedNo, count(clickLikeNo) as lastClickLikeCnt
      from (select *
            from ClickLikeTable
            where clickLikeFeedNo in (select feedNo
                                      from FeedTable
                                      where feedHost = 'bllumusic')) as lastClickLikeTable
      group by clickLikeFeedNo) as clickLikeCntByFeed
     on clickLikeCntByFeed.clickLikeFeedNo = lastClickLikeUserAndTimestamp.clickLikeFeedNo
         inner join (select feedImageFeedNo, feedImageUrl as firstUrlPerFeed
                     from (select *
                           from FeedImageTable
                           where feedimageno in
                                 (select min(feedImageNo) from FeedImageTable group by feedImageFeedNo)
                             and feedImageUserID = 'bllumusic'
                           union all
                           select *
                           from FeedVideoTable
                           where feedVideoNo in
                                 (select min(feedVideoNo) from FeedVideoTable group by feedvideoFeedNo)
                             and feedvideoUserID = 'bllumusic') as contentUrlPerFeed
                     where feedImageNo in (select min(feedImageNo)
                                           from (select *
                                                 from FeedImageTable
                                                 where feedimageno in
                                                       (select min(feedImageNo) from FeedImageTable group by feedImageFeedNo)
                                                   and feedImageUserID = 'bllumusic'
                                                 union all
                                                 select *
                                                 from FeedVideoTable
                                                 where feedVideoNo in
                                                       (select min(feedVideoNo) from FeedVideoTable group by feedvideoFeedNo)
                                                   and feedvideoUserID = 'bllumusic') as onlyOneUrlPerFeed
                                           group by feedImageFeedNo)) as firstFeedUrlTable
                    on firstFeedUrlTable.feedImageFeedNo = lastClickLikeUserAndTimestamp.clickLikeFeedNo
         inner join ProfileTable
                    on ProfileTable.profileUserID = lastClickLikeUserAndTimestamp.clickLikeUserID
order by clickLikeNo DESC;
```

![image](https://user-images.githubusercontent.com/43658658/133030803-8e0b1aef-ff87-4366-8e4d-22e9865f8f47.png)

> <h3>좋아요 활동 리스트(한 명씩)</h3>

``` mysql
-- 블루뮤직의 피드를 좋아요한 유저(한 명씩), 시간 순서대로 내림차순
select clickLikeFeedNo,
       clickLikeUserID,
       case
           when timestampdiff(second, clickLikeCreatedAt, current_timestamp) < 60
               then concat(timestampdiff(second, clickLikeCreatedAt, current_timestamp), '초')
           when timestampdiff(minute, clickLikeCreatedAt, current_timestamp) < 60
               then concat(timestampdiff(minute, clickLikeCreatedAt, current_timestamp), '분')
           when timestampdiff(hour, clickLikeCreatedAt, current_timestamp) < 24
               then concat(timestampdiff(hour, clickLikeCreatedAt, current_timestamp), '시간')
           when timestampdiff(day, clickLikeCreatedAt, current_timestamp) < 7
               then concat(timestampdiff(day, clickLikeCreatedAt, current_timestamp), '일')
           else date_format(clickLikeCreatedAt, '%m월 %d일')
           end as lastFeedTimestamp
from ClickLikeTable
where clickLikeFeedNo in (select feedNo
                          from FeedTable
                          where feedHost = 'bllumusic')
order by clickLikeNo DESC;

-- 유저 프로필 이미지, 피드 이미지를 추가한 좋아요 활동 리스트(한 명씩)
select profileImageUrl,
       concat(clickLikeUserID, '님이 회원님의 게시물을 좋아합니다.') as actClickLikeUser,
       lastFeedTimestamp,
       firstUrlPerFeed
from (select clickLikeNo,
             clickLikeFeedNo,
             clickLikeUserID,
             case
                 when timestampdiff(second, clickLikeCreatedAt, current_timestamp) < 60
                     then concat(timestampdiff(second, clickLikeCreatedAt, current_timestamp), '초')
                 when timestampdiff(minute, clickLikeCreatedAt, current_timestamp) < 60
                     then concat(timestampdiff(minute, clickLikeCreatedAt, current_timestamp), '분')
                 when timestampdiff(hour, clickLikeCreatedAt, current_timestamp) < 24
                     then concat(timestampdiff(hour, clickLikeCreatedAt, current_timestamp), '시간')
                 when timestampdiff(day, clickLikeCreatedAt, current_timestamp) < 7
                     then concat(timestampdiff(day, clickLikeCreatedAt, current_timestamp), '일')
                 else date_format(clickLikeCreatedAt, '%m월 %d일')
                 end as lastFeedTimestamp
      from ClickLikeTable
      where clickLikeFeedNo in (select feedNo
                                from FeedTable
                                where feedHost = 'bllumusic')) as clickLikeOnePerson
         inner join ProfileTable
                    on ProfileTable.profileUserID = clickLikeOnePerson.clickLikeUserID
         inner join (select feedImageFeedNo, feedImageUrl as firstUrlPerFeed
                     from (select *
                           from FeedImageTable
                           where feedimageno in
                                 (select min(feedImageNo) from FeedImageTable group by feedImageFeedNo)
                             and feedImageUserID = 'bllumusic'
                           union all
                           select *
                           from FeedVideoTable
                           where feedVideoNo in
                                 (select min(feedVideoNo) from FeedVideoTable group by feedvideoFeedNo)
                             and feedvideoUserID = 'bllumusic') as contentUrlPerFeed
                     where feedImageNo in (select min(feedImageNo)
                                           from (select *
                                                 from FeedImageTable
                                                 where feedimageno in
                                                       (select min(feedImageNo) from FeedImageTable group by feedImageFeedNo)
                                                   and feedImageUserID = 'bllumusic'
                                                 union all
                                                 select *
                                                 from FeedVideoTable
                                                 where feedVideoNo in
                                                       (select min(feedVideoNo) from FeedVideoTable group by feedvideoFeedNo)
                                                   and feedvideoUserID = 'bllumusic') as onlyOneUrlPerFeed
                                           group by feedImageFeedNo)) as firstContentPerFeed
                    on firstContentPerFeed.feedImageFeedNo = clickLikeOnePerson.clickLikeFeedNo
order by clickLikeNo DESC;
```
