import pygame
import numpy as np
import random

pygame.init()

pygame.display.init()

screen = pygame.display.set_mode((800, 600))

WHITE = 255, 255, 255
BLACK = 0,0,0
ORANGE= 255, 127, 0

def draw_board(n, w, board):
    game_obj = []
    for i in range(n):
        for j in range(n):
            game_obj.append(pygame.draw.rect(screen, WHITE, (i * w, j * w, w ,w)))
            pygame.draw.rect(screen, BLACK, (i * w, j * w, w ,w), 1)


            if board[i][j] == "X":
                pygame.draw.line(screen, ORANGE, (i * w, j * w), (i * w + w, j * w + w), 5)
                pygame.draw.line(screen, ORANGE, (i * w + w, j * w),
                                 (i * w , j * w + w), 5)
            if board[i][j] == "O":
                pygame.draw.circle(screen, ORANGE, (i * w + w//2, j * w + w//2), w//2, 5)

    return game_obj


def main():

    n = 3
    w = 80
    running = True
    board = [["" for i in range(n)] for j in range(n) ]

    players = ['X', 'O']
    current_player = random.randint(0, 1)


    clock = pygame.time.Clock()

    while running: 

        game_obj = draw_board(n,w, board)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for obj in game_obj:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if obj.collidepoint(event.pos):
                    i = obj.x // 80
                    j = obj.y // 80
                    if board[i][j] == "":
                        board[i][j] = players[current_player]
                        current_player = (current_player + 1) % len(players)


        
        pygame.display.update()

        pygame.display.flip()

        clock.tick(30)

        screen.fill(BLACK)


main()
