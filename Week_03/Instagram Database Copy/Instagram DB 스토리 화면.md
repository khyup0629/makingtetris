# 스토리 화면

![image](https://user-images.githubusercontent.com/43658658/133195761-25d00a90-9c40-4024-a62d-c0cf6c58b864.png)

> <h3>스토리 화면(다른 사람, 24시간 이내에 올린 스토리)</h3>

``` mysql
-- 스토리 화면(다른 사람, 24시간 이내 올린 스토리)
select profileImageUrl as storyProfileImage,
       storyImageUserID as storyUserID,
       case
           when timestampdiff(second, storyImageCreatedAt, '2021-09-11 00:00:00') < 60
               then concat(timestampdiff(second, storyImageCreatedAt, '2021-09-11 00:00:00'), '초')
           when timestampdiff(minute, storyImageCreatedAt, '2021-09-11 00:00:00') < 60
               then concat(timestampdiff(minute, storyImageCreatedAt, '2021-09-11 00:00:00'), '분')
           when timestampdiff(hour, storyImageCreatedAt, '2021-09-11 00:00:00') < 24
               then concat(timestampdiff(hour, storyImageCreatedAt, '2021-09-11 00:00:00'), '시간')
           when timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 7
               then concat(timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00'), '일')
           else date_format(storyImageCreatedAt, '%m월 %d일')
           end as storyUploadTime,
       storyImageUrl as storyContent
from (select *
      from StoryImageTable
      where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
      union all
      select *
      from StoryVideoTable
      where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1) as allContentStory
         inner join ProfileTable
                    on profileUserID = storyImageUserID
where storyImageUserID != 'bllumusic'
order by storyImageStoryNo DESC;
```

![image](https://user-images.githubusercontent.com/43658658/133197177-88f928b3-0d1a-4f25-a49f-94bdb23b9c57.png)

> <h3>내 스토리 화면(24시간 이내에 올린 것만)</h3>

``` mysql
-- 24시간 이내에 올린 내 스토리의 스토리 번호
select storyImageStoryNo
from StoryImageTable
where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
  and storyImageUserID = 'bllumusic'
union all
select storyVideoStoryNo
from StoryVideoTable
where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
  and storyVideoUserID = 'bllumusic';

-- 내 스토리를 본 시청자 목록
select *
from StoryWatchingTable
where storyWatchingStoryNo = (select storyImageStoryNo
                              from StoryImageTable
                              where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                and storyImageUserID = 'bllumusic'
                              union all
                              select storyVideoStoryNo
                              from StoryVideoTable
                              where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                and storyVideoUserID = 'bllumusic');

-- 내 스토리를 본 시청자 수
select storyWatchingStoryNo, count(storyWatchingUserID)
from (select *
      from StoryWatchingTable
      where storyWatchingStoryNo = (select storyImageStoryNo
                                    from StoryImageTable
                                    where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                      and storyImageUserID = 'bllumusic'
                                    union all
                                    select storyVideoStoryNo
                                    from StoryVideoTable
                                    where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                      and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
group by storyWatchingStoryNo;

-- 내 스토리를 가장 최근에 시청한 시청 여부 고유 번호
select storyWatchingStoryNo, max(storyWatchingNo) as lastBllumusicStoryWatching
from (select *
      from StoryWatchingTable
      where storyWatchingStoryNo = (select storyImageStoryNo
                                    from StoryImageTable
                                    where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                      and storyImageUserID = 'bllumusic'
                                    union all
                                    select storyVideoStoryNo
                                    from StoryVideoTable
                                    where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                      and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
group by storyWatchingStoryNo;

-- 내 스토리를 가장 최근에 시청한 유저 프로필 이미지
select storyWatchingNo, storyWatchingStoryNo, storyWatchingUserID, profileImageUrl
from StoryWatchingTable
         inner join ProfileTable
                    on profileUserID = storyWatchingUserID
where storyWatchingNo in (select max(storyWatchingNo) as lastBllumusicStoryWatching
                          from (select *
                                from StoryWatchingTable
                                where storyWatchingStoryNo = (select storyImageStoryNo
                                                              from StoryImageTable
                                                              where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                and storyImageUserID = 'bllumusic'
                                                              union all
                                                              select storyVideoStoryNo
                                                              from StoryVideoTable
                                                              where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                          group by storyWatchingStoryNo);

-- 내 스토리를 가장 최근에 시청한 유저를 제외한 시청 여부 리스트
select *
from StoryWatchingTable
where storyWatchingNo not in (select max(storyWatchingNo) as lastBllumusicStoryWatching
                              from (select *
                                    from StoryWatchingTable
                                    where storyWatchingStoryNo = (select storyImageStoryNo
                                                                  from StoryImageTable
                                                                  where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                    and storyImageUserID = 'bllumusic'
                                                                  union all
                                                                  select storyVideoStoryNo
                                                                  from StoryVideoTable
                                                                  where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                    and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                              group by storyWatchingStoryNo);

-- 내 스토리를 가장 최근에서 두 번째로 시청한 고유 번호
select storyWatchingStoryNo, max(storyWatchingNo)
from (select *
      from StoryWatchingTable
      where storyWatchingNo not in (select max(storyWatchingNo) as lastBllumusicStoryWatching
                                    from (select *
                                          from StoryWatchingTable
                                          where storyWatchingStoryNo = (select storyImageStoryNo
                                                                        from StoryImageTable
                                                                        where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                          and storyImageUserID = 'bllumusic'
                                                                        union all
                                                                        select storyVideoStoryNo
                                                                        from StoryVideoTable
                                                                        where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                          and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                                    group by storyWatchingStoryNo)
        and storyWatchingHost = 'bllumusic') as bllumusicSecondStoryWatcher
group by storyWatchingStoryNo;

-- 내 스토리를 가장 최근에서 두 번째로 본 유저의 프로필 이미지
select storyWatchingNo, storyWatchingStoryNo, storyWatchingUserID, profileImageUrl
from (select *
      from StoryWatchingTable
      where storyWatchingNo not in (select max(storyWatchingNo) as lastBllumusicStoryWatching
                                    from (select *
                                          from StoryWatchingTable
                                          where storyWatchingStoryNo = (select storyImageStoryNo
                                                                        from StoryImageTable
                                                                        where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                          and storyImageUserID = 'bllumusic'
                                                                        union all
                                                                        select storyVideoStoryNo
                                                                        from StoryVideoTable
                                                                        where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                          and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                                    group by storyWatchingStoryNo)) as notInlastBllumusicStoryWatching
         inner join ProfileTable
                    on profileUserID = storyWatchingUserID
where storyWatchingNo in (select max(storyWatchingNo)
                          from (select *
                                from StoryWatchingTable
                                where storyWatchingNo not in (select max(storyWatchingNo) as lastBllumusicStoryWatching
                                                              from (select *
                                                                    from StoryWatchingTable
                                                                    where storyWatchingStoryNo =
                                                                          (select storyImageStoryNo
                                                                           from StoryImageTable
                                                                           where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                             and storyImageUserID = 'bllumusic'
                                                                           union all
                                                                           select storyVideoStoryNo
                                                                           from StoryVideoTable
                                                                           where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                             and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                                                              group by storyWatchingStoryNo)
                                  and storyWatchingHost = 'bllumusic') as bllumusicSecondStoryWatcher
                          group by storyWatchingStoryNo);

-- 블루뮤직의 스토리별 가장 최근에 본 시청자 프로필 이미지 묶기
select storyWatchingStoryNo, group_concat(profileImageUrl, '') as lastBllumusicStoryWatcher
from (select storyWatchingNo, storyWatchingStoryNo, storyWatchingUserID, profileImageUrl
      from StoryWatchingTable
               inner join ProfileTable
                          on profileUserID = storyWatchingUserID
      where storyWatchingNo in (select max(storyWatchingNo) as lastBllumusicStoryWatching
                                from (select *
                                      from StoryWatchingTable
                                      where storyWatchingStoryNo = (select storyImageStoryNo
                                                                    from StoryImageTable
                                                                    where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                      and storyImageUserID = 'bllumusic'
                                                                    union all
                                                                    select storyVideoStoryNo
                                                                    from StoryVideoTable
                                                                    where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                      and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                                group by storyWatchingStoryNo)
      union all
      select storyWatchingNo, storyWatchingStoryNo, storyWatchingUserID, profileImageUrl
      from (select *
            from StoryWatchingTable
            where storyWatchingNo not in (select max(storyWatchingNo) as lastBllumusicStoryWatching
                                          from (select *
                                                from StoryWatchingTable
                                                where storyWatchingStoryNo = (select storyImageStoryNo
                                                                              from StoryImageTable
                                                                              where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                                and storyImageUserID = 'bllumusic'
                                                                              union all
                                                                              select storyVideoStoryNo
                                                                              from StoryVideoTable
                                                                              where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                                and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                                          group by storyWatchingStoryNo)) as notInlastBllumusicStoryWatching
               inner join ProfileTable
                          on profileUserID = storyWatchingUserID
      where storyWatchingNo in (select max(storyWatchingNo)
                                from (select *
                                      from StoryWatchingTable
                                      where storyWatchingNo not in
                                            (select max(storyWatchingNo) as lastBllumusicStoryWatching
                                             from (select *
                                                   from StoryWatchingTable
                                                   where storyWatchingStoryNo =
                                                         (select storyImageStoryNo
                                                          from StoryImageTable
                                                          where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                            and storyImageUserID = 'bllumusic'
                                                          union all
                                                          select storyVideoStoryNo
                                                          from StoryVideoTable
                                                          where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                            and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                                             group by storyWatchingStoryNo)
                                        and storyWatchingHost = 'bllumusic') as bllumusicSecondStoryWatcher
                                group by storyWatchingStoryNo)) as lastBllumusicStoryWatcherTable
group by storyWatchingStoryNo;

-- 내 스토리 화면(24시간 이내 올린 스토리)
select ProfileTable.profileImageUrl as storyProfileImage,
       storyImageUserID             as storyUserID,
       case
           when timestampdiff(second, storyImageCreatedAt, '2021-09-11 00:00:00') < 60
               then concat(timestampdiff(second, storyImageCreatedAt, '2021-09-11 00:00:00'), '초')
           when timestampdiff(minute, storyImageCreatedAt, '2021-09-11 00:00:00') < 60
               then concat(timestampdiff(minute, storyImageCreatedAt, '2021-09-11 00:00:00'), '분')
           when timestampdiff(hour, storyImageCreatedAt, '2021-09-11 00:00:00') < 24
               then concat(timestampdiff(hour, storyImageCreatedAt, '2021-09-11 00:00:00'), '시간')
           when timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 7
               then concat(timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00'), '일')
           else date_format(storyImageCreatedAt, '%m월 %d일')
           end                      as storyUploadTime,
       storyImageUrl                as storyContent,
       lastBllumusicStoryWatcher,
       bllumusicStoryWatcherCnt
from (select *
      from StoryImageTable
      where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
        and storyImageUserID = 'bllumusic'
      union all
      select *
      from StoryVideoTable
      where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
        and storyVideoUserID = 'bllumusic') as allContentStory
         inner join ProfileTable
                    on profileUserID = storyImageUserID
         inner join (select storyWatchingStoryNo, group_concat(profileImageUrl, '') as lastBllumusicStoryWatcher
                     from (select storyWatchingNo, storyWatchingStoryNo, storyWatchingUserID, profileImageUrl
                           from StoryWatchingTable
                                    inner join ProfileTable
                                               on profileUserID = storyWatchingUserID
                           where storyWatchingNo in (select max(storyWatchingNo) as lastBllumusicStoryWatching
                                                     from (select *
                                                           from StoryWatchingTable
                                                           where storyWatchingStoryNo = (select storyImageStoryNo
                                                                                         from StoryImageTable
                                                                                         where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                                           and storyImageUserID = 'bllumusic'
                                                                                         union all
                                                                                         select storyVideoStoryNo
                                                                                         from StoryVideoTable
                                                                                         where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                                           and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                                                     group by storyWatchingStoryNo)
                           union all
                           select storyWatchingNo, storyWatchingStoryNo, storyWatchingUserID, profileImageUrl
                           from (select *
                                 from StoryWatchingTable
                                 where storyWatchingNo not in (select max(storyWatchingNo) as lastBllumusicStoryWatching
                                                               from (select *
                                                                     from StoryWatchingTable
                                                                     where storyWatchingStoryNo =
                                                                           (select storyImageStoryNo
                                                                            from StoryImageTable
                                                                            where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                              and storyImageUserID = 'bllumusic'
                                                                            union all
                                                                            select storyVideoStoryNo
                                                                            from StoryVideoTable
                                                                            where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                              and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                                                               group by storyWatchingStoryNo)) as notInlastBllumusicStoryWatching
                                    inner join ProfileTable
                                               on profileUserID = storyWatchingUserID
                           where storyWatchingNo in (select max(storyWatchingNo)
                                                     from (select *
                                                           from StoryWatchingTable
                                                           where storyWatchingNo not in
                                                                 (select max(storyWatchingNo) as lastBllumusicStoryWatching
                                                                  from (select *
                                                                        from StoryWatchingTable
                                                                        where storyWatchingStoryNo =
                                                                              (select storyImageStoryNo
                                                                               from StoryImageTable
                                                                               where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                                                 and storyImageUserID = 'bllumusic'
                                                                               union all
                                                                               select storyVideoStoryNo
                                                                               from StoryVideoTable
                                                                               where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                                                 and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                                                                  group by storyWatchingStoryNo)
                                                             and storyWatchingHost = 'bllumusic') as bllumusicSecondStoryWatcher
                                                     group by storyWatchingStoryNo)) as lastBllumusicStoryWatcherTable
                     group by storyWatchingStoryNo) as lastStoryWatcherTable
                    on lastStoryWatcherTable.storyWatchingStoryNo = allContentStory.storyImageStoryNo
         inner join (select storyWatchingStoryNo, count(storyWatchingUserID) as bllumusicStoryWatcherCnt
                     from (select *
                           from StoryWatchingTable
                           where storyWatchingStoryNo = (select storyImageStoryNo
                                                         from StoryImageTable
                                                         where timestampdiff(day, storyImageCreatedAt, '2021-09-11 00:00:00') < 1
                                                           and storyImageUserID = 'bllumusic'
                                                         union all
                                                         select storyVideoStoryNo
                                                         from StoryVideoTable
                                                         where timestampdiff(day, storyVideoCreatedAt, '2021-09-11 00:00:00') < 1
                                                           and storyVideoUserID = 'bllumusic')) as bllumusicStoryWatcher
                     group by storyWatchingStoryNo) as bllumusicStoryWatcherCntTable
                    on bllumusicStoryWatcherCntTable.storyWatchingStoryNo = allContentStory.storyImageStoryNo
order by storyImageStoryNo DESC;
```

![image](https://user-images.githubusercontent.com/43658658/133201316-fa0234ff-cdee-43d6-9e44-1f55315858b7.png)
