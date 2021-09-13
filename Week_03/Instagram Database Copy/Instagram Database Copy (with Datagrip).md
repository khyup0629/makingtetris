# 타임라인 화면

![image](https://user-images.githubusercontent.com/43658658/132867830-2b43d479-e39a-40ef-b70a-ba6393e83046.png)

> <h3>스토리 리스트</h3>

``` mysql
-- 스토리 리스트 : 내(bllumusic) 스토리 표시(스토리는 24시간 이내 올린 스토리만 노출)
select profileImageurl as storyProfileImage,
       if(exists(select *
                 from StoryTable
                 where timestampdiff(day, storyCreatedAt, current_timestamp) < 1
                   and storyUserID = 'bllumusic'
                 order by storyNo DESC)
              and
          (select storyNo
           from StoryTable
           where timestampdiff(day, storyCreatedAt, current_timestamp) < 1
             and storyUserID = 'bllumusic'
           order by storyNo DESC)
              in (select storyWatchingStoryNo from StoryWatchingTable where storyWatchingUserID = 'bllumusic'),
          'Y', 'N')    as storyIsWatchingMyself
from ProfileTable
where profileUserID = 'bllumusic';
```

![image](https://user-images.githubusercontent.com/43658658/132847659-86841857-bd95-4b32-b1df-ca9bf9262cde.png)

``` mysql
-- 스토리 리스트 : 내(bllumusic)가 팔로우한 유저들 스토리 표시 (스토리는 24시간 이내 올린 스토리만 노출)
select storyNo,
       profileImageUrl                                                    as storyFollowProfileImage,
       profileUserID                                                      as storyFollowUserID,
       if(storyNo in (select storyWatchingStoryNo
                      from StoryWatchingTable
                      where storyWatchingUserID = 'bllumusic'), 'Y', 'N') as storyIsWatching
from (select max(storyNo) as storyNo, storyUserID
      from StoryTable
      where timestampdiff(day, storyCreatedAt, current_timestamp) < 1
      group by storyUserID) as StoryWithinDayTable
         inner join (select *
                     from FollowerTable
                     where followerUserID = 'bllumusic') as followerBllumusic
                    on followerBllumusic.followerHost = StoryWithinDayTable.storyUserID
         inner join ProfileTable
                    on ProfileTable.profileUserID = StoryWithinDayTable.storyUserID
order by storyNo DESC;
```

![image](https://user-images.githubusercontent.com/43658658/132847785-f03fd450-d60f-4d61-a484-b82ff5125b71.png)

> <h3>타임라인</h3>

``` mysql
-- 피드에 맞는 사진, 동영상
select feedImageUrl as feedImageVideoUrl
from FeedImageTable
where feedImageUserID = 'bllumusic'
  and feedImageFeedNo = 4
union
select feedVideoUrl as feedImageVideoUrl
from FeedVideoTable
where feedVideoUserID = 'bllumusic'
  and feedVideoFeedNo = 4;
```

![image](https://user-images.githubusercontent.com/43658658/132867724-5bf41e5f-32f6-46d7-a88d-66f6f0b01c94.png)

``` mysql
-- 사진, 동영상을 제외한 나머지 타임라인 피드, 내(bllumusic)가 팔로우한 유저의 피드만 띄운다.
select feedNo,
       profileImageUrl,
       feedHost,
       if(feedNo in (select clickLikeFeedNo from ClickLikeTable group by clickLikeFeedNo),
          if((select count(clickLikeNo) as clickLikeCnt
              from ClickLikeTable
              where clickLikeFeedNo = feedNo
              group by clickLikeFeedNo) >= 2,
             concat((select clickLikeUserID
                     from ClickLikeTable
                     where clickLikeNo =
                           (select max(clickLikeNo)
                            from ClickLikeTable
                            where clickLikeFeedNo = FeedTable.feedNo
                            group by clickLikeFeedNo)),
                    '외 ', (select count(clickLikeNo) as clickLikeCnt
                           from ClickLikeTable
                           where clickLikeFeedNo = feedNo
                           group by clickLikeFeedNo) - 1, '명이 좋아합니다.'),
             concat((select clickLikeUserID as clickLikeCnt
                     from ClickLikeTable
                     where clickLikeFeedNo = feedNo), '님이 좋아합니다.')), '')
                                                                        as clickLikeCnt,
       feedContent,
       if(feedNo in (select replyFeedNo from ReplyTable group by replyFeedNo),
          if((select count(replyFeedNo) as replyCnt
              from ReplyTable
              where replyFeedNo = feedNo
              group by replyFeedNo) >= 1,
             concat('댓글 ', (select count(replyFeedNo) as replyCnt
                            from ReplyTable
                            where replyFeedNo = feedNo
                            group by replyFeedNo), '개 모두 보기'), ''), '') as replyCnt,
       case
           when timestampdiff(second, feedCreatedAt, current_timestamp) <= 59
               then '방금 전'
           when timestampdiff(minute, feedCreatedAt, current_timestamp) <= 59
               then concat(timestampdiff(minute, feedCreatedAt, current_timestamp), '분 전')
           when timestampdiff(hour, feedCreatedAt, current_timestamp) <= 23
               then concat(timestampdiff(hour, feedCreatedAt, current_timestamp), '시간 전')
           else date_format(feedCreatedAt, '%m월 %d일')
           end                                                          as feedCreatedAt
from FeedTable
         inner join ProfileTable
                    on profileUserID = feedHost
         inner join (select followerHost from FollowerTable where followerUserID = 'bllumusic') as followerBllumusic
                    on followerHost = feedHost
order by feedNo DESC;
```

![image](https://user-images.githubusercontent.com/43658658/132862863-b36921c6-1334-42ea-9584-4bc1098825a8.png)

# 회원님을 위한 추천

![image](https://user-images.githubusercontent.com/43658658/132868101-11c76ec7-eb03-4e5b-baef-415c789d0b51.png)

``` mysql
-- 블루뮤직과 맞팔한 유저 목록
select followerUserID
from (select followerUserID from FollowerTable where followerHost = 'bllumusic') as followerBllumusic
where followerUserID in (select followerHost from FollowerTable where followerUserID = 'bllumusic');

-- 블루뮤직과 맞팔한 유저들이 팔로잉하고 있는 유저들을 나열
select followerNo, followerHost, followerUserID
from FollowerTable
where followerUserID in (select followerUserID
                         from (select followerUserID
                               from FollowerTable
                               where followerHost = 'bllumusic') as followerBllumusic
                         where followerUserID in
                               (select followerHost from FollowerTable where followerUserID = 'bllumusic'));

-- 블루뮤직과 맞팔한 유저들이 팔로잉하고 있는 유저들을 나열하고 팔로잉 받은 수를 카운트,
select followerHost, count(followerHost) as followerCnt
from (select followerNo, followerHost, followerUserID
      from FollowerTable
      where followerUserID in (select followerUserID
                               from (select followerUserID
                                     from FollowerTable
                                     where followerHost = 'bllumusic') as followerBllumusic
                               where followerUserID in (select followerHost
                                                        from FollowerTable
                                                        where followerUserID = 'bllumusic'))) as allFollowingTable
group by followerHost;

-- 블루뮤직과 맞팔한 유저들이 팔로잉하고 있는 유저별 가장 마지막에 팔로우한 유저
select FollowerTable.followerHost, followerUserID as recoRecentOverlapUserID
from (select max(followerNo) as lastFollowerNo, followerHost
      from (select followerNo, followerHost, followerUserID
            from FollowerTable
            where followerUserID in (select followerUserID
                                     from (select followerUserID
                                           from FollowerTable
                                           where followerHost = 'bllumusic') as followerBllumusic
                                     where followerUserID in
                                           (select followerHost from FollowerTable where followerUserID = 'bllumusic'))
           ) as lastFollower
      group by followerHost
     ) as lastFollowerTable
         inner join FollowerTable
                    on followerNo = lastFollowerNo;

-- 카운트가 2이상이고, 블루뮤직(자신)이 아니며, 블루뮤직(자신)이 팔로우하지 않았으면 추천
select profileImageUrl         as recoProfileImage,
       followerHost            as recoUserID,
       if(followerCnt = 2,
          concat((select recoRecentOverlapUserID
                  from (select FollowerTable.followerHost, followerUserID as recoRecentOverlapUserID
                        from (select max(followerNo) as lastFollowerNo, followerHost
                              from (select followerNo, followerHost, followerUserID
                                    from FollowerTable
                                    where followerUserID in (select followerUserID
                                                             from (select followerUserID
                                                                   from FollowerTable
                                                                   where followerHost = 'bllumusic') as followerBllumusic
                                                             where followerUserID in (select followerHost
                                                                                      from FollowerTable
                                                                                      where followerUserID = 'bllumusic'))
                                   ) as lastFollower
                              group by followerHost
                             ) as lastFollowerTable
                                 inner join FollowerTable
                                            on followerNo = lastFollowerNo) as lastFollowerTable
                  where followerCntTable.followerHost = followerHost), '님 외 ', '1명이 팔로우합니다'),
          concat((select recoRecentOverlapUserID
                  from (select FollowerTable.followerHost, followerUserID as recoRecentOverlapUserID
                        from (select max(followerNo) as lastFollowerNo, followerHost
                              from (select followerNo, followerHost, followerUserID
                                    from FollowerTable
                                    where followerUserID in (select followerUserID
                                                             from (select followerUserID
                                                                   from FollowerTable
                                                                   where followerHost = 'bllumusic') as followerBllumusic
                                                             where followerUserID in (select followerHost
                                                                                      from FollowerTable
                                                                                      where followerUserID = 'bllumusic'))
                                   ) as lastFollower
                              group by followerHost
                             ) as lastFollowerTable
                                 inner join FollowerTable
                                            on followerNo = lastFollowerNo) as lastFollowerTable
                  where followerCntTable.followerHost = followerHost), '님 외 ', followerCnt - 1,
                 '명이 팔로우합니다')) as recoOverlapUserCnt
from (select followerHost, count(followerHost) as followerCnt
      from (select followerHost
            from FollowerTable
            where followerUserID in (select followerUserID
                                     from (select followerUserID
                                           from FollowerTable
                                           where followerHost = 'bllumusic') as followerBllumusic
                                     where followerUserID in (select followerHost
                                                              from FollowerTable
                                                              where followerUserID = 'bllumusic'))) as allFollowingTable
      group by followerHost) as followerCntTable
         inner join ProfileTable
                    on profileUserID = followerHost
where followerCnt >= 2
  and followerHost != 'bllumusic'
  and followerHost not in (select followerHost from FollowerTable where followerUserID = 'bllumusic');

-- 차집합, 블루뮤직의 팔로워 중 블루뮤직이 팔로잉하지 않은 유저 목록(맞팔 X)
select profileImageUrl, followerUserID, '회원님을 팔로우합니다.'
from (select followerUserID from FollowerTable where followerHost = 'bllumusic') as followerBllumusic
         inner join ProfileTable
                    on profileUserID = followerUserID
where followerUserID not in (select followerHost from FollowerTable where followerUserID = 'bllumusic');

-- 두 추천 조건을 모두 합친 유저 목록
select profileImageUrl         as recoProfileImage,
       followerHost            as recoUserID,
       if(followerCnt = 2,
          concat((select recoRecentOverlapUserID
                  from (select FollowerTable.followerHost, followerUserID as recoRecentOverlapUserID
                        from (select max(followerNo) as lastFollowerNo, followerHost
                              from (select followerNo, followerHost, followerUserID
                                    from FollowerTable
                                    where followerUserID in (select followerUserID
                                                             from (select followerUserID
                                                                   from FollowerTable
                                                                   where followerHost = 'bllumusic') as followerBllumusic
                                                             where followerUserID in (select followerHost
                                                                                      from FollowerTable
                                                                                      where followerUserID = 'bllumusic'))
                                   ) as lastFollower
                              group by followerHost
                             ) as lastFollowerTable
                                 inner join FollowerTable
                                            on followerNo = lastFollowerNo) as lastFollowerTable
                  where followerCntTable.followerHost = followerHost), '님 외 ', '1명이 팔로우합니다'),
          concat((select recoRecentOverlapUserID
                  from (select FollowerTable.followerHost, followerUserID as recoRecentOverlapUserID
                        from (select max(followerNo) as lastFollowerNo, followerHost
                              from (select followerNo, followerHost, followerUserID
                                    from FollowerTable
                                    where followerUserID in (select followerUserID
                                                             from (select followerUserID
                                                                   from FollowerTable
                                                                   where followerHost = 'bllumusic') as followerBllumusic
                                                             where followerUserID in (select followerHost
                                                                                      from FollowerTable
                                                                                      where followerUserID = 'bllumusic'))
                                   ) as lastFollower
                              group by followerHost
                             ) as lastFollowerTable
                                 inner join FollowerTable
                                            on followerNo = lastFollowerNo) as lastFollowerTable
                  where followerCntTable.followerHost = followerHost), '님 외 ', followerCnt - 1,
                 '명이 팔로우합니다')) as recoOverlapUserCnt
from (select followerHost, count(followerHost) as followerCnt
      from (select followerHost
            from FollowerTable
            where followerUserID in (select followerUserID
                                     from (select followerUserID
                                           from FollowerTable
                                           where followerHost = 'bllumusic') as followerBllumusic
                                     where followerUserID in (select followerHost
                                                              from FollowerTable
                                                              where followerUserID = 'bllumusic'))) as allFollowingTable
      group by followerHost) as followerCntTable
         inner join ProfileTable
                    on profileUserID = followerHost
where followerCnt >= 2
  and followerHost != 'bllumusic'
  and followerHost not in (select followerHost from FollowerTable where followerUserID = 'bllumusic')
union
select profileImageUrl, followerUserID, '회원님을 팔로우합니다.'
from (select followerUserID from FollowerTable where followerHost = 'bllumusic') as followerBllumusic
         inner join ProfileTable
                    on profileUserID = followerUserID
where followerUserID not in (select followerHost from FollowerTable where followerUserID = 'bllumusic');
```

![image](https://user-images.githubusercontent.com/43658658/132893641-cb1f4a9c-8215-4126-803d-78276c557f93.png)

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
