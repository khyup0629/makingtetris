# -*- coding: utf-8 -*-

from random import randrange as rand
import pygame
import sys

cell_size = 18
cols = 10
rows = 22
maxfps = 30

# https://convertingcolors.com/rgb-color-0_0_0.html?search=RGB(0,%200,%200)
# 위의 사이트에서 RGB 색상 확인 가능
colors = [(0, 0, 0),  # 검정색
          (255, 85, 85),  # 분홍색
          (100, 200, 115),  # 초록색
          (120, 108, 245),  # 파란색
          (255, 140, 50),  # 주황색
          (50, 120, 52),  # 녹색
          (146, 202, 73),  # 연두색
          (150, 161, 218),  # 하늘색
          (35, 35, 35)]  # 진한 회색

tetris_shapes = [[[1, 1, 1],
                  [0, 1, 0]],

                 [[0, 2, 2],
                  [2, 2, 0]],

                 [[3, 3, 0],
                  [0, 3, 3]],

                 [[4, 0, 0],
                  [4, 4, 4]],

                 [[0, 0, 5],
                  [5, 5, 5]],

                 [[6, 6, 6, 6]],

                 [[7, 7],
                  [7, 7]]]


# 시계 방향으로 블럭 돌리기
def rotate_clockwise(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]


# 블럭의 충돌 여부 체크
def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):  # index, value
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


# 줄 지우기
def remove_row(board, row):
    del board[row]  # 전체 판에서 한 줄을 지우고
    return [[0 for i in range(cols)]] + board  # 전체 판에 빈(0) 줄을 맨 위에 추가


#
def join_matrixes(board, stone, stone_off):
    off_x, off_y = stone_off
    for cy, row in enumerate(stone):
        for cx, val in enumerate(row):
            board[cy + off_y - 1][cx + off_x] += val
    return board


# 새로운 판 생성
def new_board():
    board = [[0 for x in range(cols)] for y in range(rows)]
    board += [[1 for x in range(cols)]]
    return board


class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 25)  # 누르고 있는 키의 반복을 제어 (지연시간, 간격)
        # 키를 누르면 첫 번째 이벤트 발생, 키다운하고 있으면 지연시간 이후 두 번째 이벤트 발생
        # 이후 간격마다 이벤트 발생
        self.width = cell_size * (cols + 6)
        self.height = cell_size * rows
        self.rlim = cell_size * cols
        self.bground_grid = [[8 if x % 2 == y % 2 else 0 for x in range(cols)] for y in range(rows)]

        self.default_font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)  # 마우스 움직임을 제한한다.
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]  # 0~6 사이의 수를 무작위 생성
        self.init_game()

    def new_stone(self):  # 새로운 블럭이 나올 때
        self.stone = self.next_stone[:]  # 새로운 블록
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]  # 다음 블록
        self.stone_x = int(cols / 2 - len(self.stone[0]) / 2)  # 새로운 블록 생성 위치 x 좌표
        self.stone_y = 0  # 새로운 블록 생성 위치 y 좌표
        # 새로운 블록이 생성되자마자 게임 오버가 될 수도 있다.
        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()  # 새로운 판 생성
        self.new_stone()  # 새로운 블록 생성
        self.level = 1  # 레벨
        self.score = 0  # 점수
        self.lines = 0  # 지운 라인 개수
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    def disp_msg(self, msg, topleft):  # 게임창에 텍스트를 출력한다.
        x, y = topleft
        for line in msg.splitlines():
            self.screen.blit(self.default_font.render(line, False, (255, 255, 255), (0, 0, 0)), (x, y))
            y += 14

    def center_msg(self, msg):  # 가운데에 메세지 출력, msg : 메세지 내용
        # splitlines : 텍스트를 각 줄을 리스트의 원소로 나눈다.
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.default_font.render(line, False, (255, 255, 255), (0, 0, 0))
            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
            # 마지막에 i * 22는 텍스트의 줄마다 간격을 띄우기 위함임.
            self.screen.blit(msg_image, (self.width // 2 - msgim_center_x, self.height // 2 - msgim_center_y + i * 22))

    def draw_matrix(self, matrix, offset):  # 움직이는 물체(사각형) 생성, 맵과 블록 모두 사각형.
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    # screen에 RGB 색상으로 사각형(rect) 생성
                    # pygame.Rect(x, y, w, h) : 사각형 좌상단 (x, y) 좌표와 너비(w)와 높이(h)
                    pygame.draw.rect(self.screen, colors[val],
                                     pygame.Rect((off_x + x) * cell_size,
                                                 (off_y + y) * cell_size, cell_size, cell_size), 0)

    def add_cl_lines(self, n):  # 한 번에 지운 라인 수(n)으로 지운 라인 수와 점수 갱신
        linescores = [0, 40, 100, 300, 1200]  # 테트리스 게임은 한 번에 최대 4개의 라인까지 지울 수 있다.
        self.lines += n
        self.score += linescores[n] * self.level  # 점수는 한 번에 지운 라인 수(n) * 레벨
        if self.lines >= self.level * 6:  # 레벨업의 기준은 레벨 * 6 이상의 라인을 지울 때.
            self.level += 1
            # 아래로 자동으로 떨어지는 빠르기가 레벨에 따라 상승. delay가 작을 수록 빠르기 상승
            newdelay = 1000 - 50 * (self.level - 1)
            newdelay = 100 if newdelay < 100 else newdelay  # 최대 빠르기 설정
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)  # time set 갱신

    def move(self, delta_x):  # 좌우로의 블록 움직임
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:  # 왼쪽으로의 움직임이 왼쪽 끝을 넘어서면,
                new_x = 0
            if new_x > cols - len(self.stone[0]):  # 오른쪽으로의 움직임이 오른쪽 끝을 넘어서면,
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x

    def drop(self, manual):  # 일정 시간 간격으로 아래로 떨어지는 움직임
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            # 내려가다가 블록이 쌓이면
            if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0  # 이번 블록이 쌓이면서 지워지는 라인 개수
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:  # 라인이 꽉 찼다면 (비워진 칸은 0)
                            self.board = remove_row(self.board, i)  # 라인이 지워진 board 갱신
                            cleared_rows += 1  # 지운 라인 개수
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def insta_drop(self):  # ???
        if not self.gameover and not self.paused:
            while not self.drop(True):
                pass

    def rotate_stone(self):  # 블록 회전
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):  # 일시 정지
        self.paused = not self.paused

    def quit(self):  # 게임을 종료할 때.
        self.center_msg("Exiting...")  # 메세지를 가운데에 출력
        pygame.display.update()
        sys.exit()

    def start_game(self):  # 게임이 종료되면 새로 시작
        if self.gameover:
            self.init_game()
            self.gameover = False

    def run(self):
        key_actions = {'ESCAPE': self.quit,
                       'LEFT': lambda: self.move(-1),
                       'RIGHT': lambda: self.move(+1),
                       'DOWN': lambda: self.drop(True),
                       'UP': self.rotate_stone,
                       'p': self.toggle_pause,
                       'SPACE': self.insta_drop,
                       'RETURN': self.start_game}
        self.gameover = False
        self.paused = False

        dont_burn_cpu = pygame.time.Clock()
        while True:
            self.screen.fill((0, 0, 0))
            if self.gameover:  # 게임 오버되면 게임 오버 메세지 띄우기
                self.center_msg("""Game Over!\nYour score: %d
                Press \'enter\' to continue""" % self.score)
            else:
                if self.paused:  # 'p' 키를 누르면 일시 정지 메세지 띄우기
                    # 위의 함수들에도 not.paused 를 조건으로 걸어서, 뒤에서 자동으로 움직이지 않도록 했다.
                    self.center_msg("Paused")
                else:  # 게임화면 표시
                    pygame.draw.line(self.screen, (255, 255, 255), (self.rlim+1, 0), (self.rlim+1, self.height-1))
                    self.disp_msg("Next", (self.rlim+cell_size, 2))
                    self.disp_msg("Score: %d\n\nLevel: %d\nLines: %d" % (self.score, self.level, self.lines),
                                  (self.rlim+cell_size, cell_size*5))
                    self.draw_matrix(self.bground_grid, (0, 0))
                    self.draw_matrix(self.board, (0, 0))
                    self.draw_matrix(self.stone, (self.stone_x, self.stone_y))
                    self.draw_matrix(self.next_stone, (cols+1, 2))
            pygame.display.update()

            for event in pygame.event.get():  # pygame 에서 이벤트 발생.
                if event.type == pygame.USEREVENT+1:  # 가만히 있을 때,
                    self.drop(False)  # 자동으로 1칸 씩 내려오도록
                elif event.type == pygame.QUIT:  # 멈췄을 때,
                    self.quit()  # 종료.
                elif event.type == pygame.KEYDOWN:  # 키를 누르면,
                    for key in key_actions:  # 게임에서 활성화된 키를 하나씩 탐색.
                        if event.key == eval("pygame.K_"+key):  # 누른 키와 같다면,
                            key_actions[key]()  # 키에 해당하는 함수를 실행.
                            # 딕셔너리의 value 가 함수이므로 뒤에 ()를 붙여준다.

            dont_burn_cpu.tick(maxfps)  # 최대 프레임 수 설정.


if __name__ == '__main__':
    App = TetrisApp()
    App.run()

