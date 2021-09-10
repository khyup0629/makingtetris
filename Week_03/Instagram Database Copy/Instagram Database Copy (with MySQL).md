

``` mysql
-- 스토리 리스트 : 내(bllumusic) 스토리 표시(스토리는 24시간 이내 올린 스토리만 노출)
select profileImageurl as storyProfileImage,
       if(exists(select * from StoryTable where timestampdiff(day, storyCreatedAt, current_timestamp) < 1
                    and storyUserID = 'bllumusic' order by storyNo DESC)
        and
          (select storyNo from StoryTable where timestampdiff(day, storyCreatedAt, current_timestamp) < 1
            and storyUserID = 'bllumusic' order by storyNo DESC)
            in (select storyWatchingStoryNo from StoryWatchingTable where storyWatchingUserID = 'bllumusic'),
           'Y', 'N') as storyIsWatchingMyself
from ProfileTable
where profileUserID = 'bllumusic';
```

![image](https://user-images.githubusercontent.com/43658658/132847659-86841857-bd95-4b32-b1df-ca9bf9262cde.png)

``` mysql
-- 스토리 리스트 : 내(bllumusic)가 팔로우한 유저들 스토리 표시 (스토리는 24시간 이내 올린 스토리만 노출)
select storyNo, profileImageUrl as storyFollowProfileImage, profileUserID as storyFollowUserID,
       if (storyNo in (select storyWatchingStoryNo
                        from StoryWatchingTable
                        where storyWatchingUserID = 'bllumusic'), 'Y', 'N') as storyIsWatching
from (select max(storyNo) as storyNo, storyUserID from StoryTable
    where timestampdiff(day, storyCreatedAt, current_timestamp) < 1 group by storyUserID) as StoryWithinDayTable
inner join (select *
from FollowerTable
where followerUserID = 'bllumusic') as followerBllumusic
on followerBllumusic.followerHost = StoryWithinDayTable.storyUserID
inner join ProfileTable
on ProfileTable.profileUserID = StoryWithinDayTable.storyUserID
order by storyNo DESC;
```

![image](https://user-images.githubusercontent.com/43658658/132847785-f03fd450-d60f-4d61-a484-b82ff5125b71.png)
