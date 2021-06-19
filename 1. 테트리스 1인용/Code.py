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
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0])-1, -1, -1)]


# 블럭 왼쪽, 오른쪽으로 옮기기
def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):  # index, value
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy+off_y][cx+off_x]:
                    return True
            except IndexError:
                return True
    return False


# 줄 지우기
def remove_row(board, row):
    del board[row]  # 전체 판에서 한 줄을 지우고
    return [[0 for i in range(cols)]] + board  # 전체 판에 빈(0) 줄을 맨 위에 추가

