# 1. 테트리스 1인용 만들기

## pygame 설치

+ 파이썬 IDE의 터미널에서 아래의 명령어를 입력해 pygame 라이브러리를 설치한다.

```
pip install pygame
```
## pygame 함수 정리

+ pygame.key.set_repeat(delaytime, interval) : 키다운을 할 때 첫 번째 이벤트 이후 delaytime 이후 두 번째 이벤트가 일어나고, 세 번째 이벤트부터는 interval 시간 간격마다 이벤트가 일어난다.
+ pygame.display.set_mode((width, height)) : 게임 창의 크기를 결정한다.
+ pygame.event.set_blocked(pygame.MOUSEMOTION) : 게임 내에서 벌어질 수 있는 어떤 행위들을 막는다.
  + pygame.MOUSEMOTION : 마우스의 움직임
+ pygame.time.set_timer(eventid, millseconds) : 움직임(eventid)이 millseconds마다 벌어지도록 할 때 사용
+ pygame에서 메세지 나타내기
  + 1. font 설정
    + pygame.font.Font(글꼴, 크기) : 게임의 글꼴을 설정한다.
      + pygame.font.get_default_font() : 파이게임의 디폴트 글꼴
  + 2. render 설정 : 문자열을 이미지로 바꿔준다.
    + font.render(문자열, 안티앨리어싱 여부, 색상)
  + 3. blit 설정
    + screen.blit(img, rect) : 이미지(img)를 사각형의 좌상단 위치(x, y)에 복사한다.
+ pygame.draw.rect(screen, RGB, pygame.Rect(x, y, w, h)) : screen에 RGB 색상으로 사각형 생성
  + pygame.Rect(x, y, w, h) : 사각형 좌상단 (x, y) 좌표와 너비(w)와 높이(h)
+ pygame.draw.line(screen, RGB, 시작점(x, y), 끝점(x, y)) : 시작점에서 끝점까지 RGB 색상으로 선을 그린다.
---
[참조]
+ https://comsperger.tistory.com/323
