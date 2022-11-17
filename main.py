import pygame
import numpy as np
import random

pygame.init()

pygame.display.init()

screen = pygame.display.set_mode((800, 600))

WHITE = 255, 255, 255
BLACK = 0, 0, 0
ORANGE = 255, 127, 0


def draw_board(n, w, board):
    game_obj = []
    for i in range(n):
        for j in range(n):
            game_obj.append(pygame.draw.rect(
                screen, WHITE, (i * w, j * w, w, w)))
            pygame.draw.rect(screen, BLACK, (i * w, j * w, w, w), 1)

            if board[i][j] == "X":
                pygame.draw.line(screen, ORANGE, (i * w, j * w),
                                 (i * w + w, j * w + w), 5)
                pygame.draw.line(screen, ORANGE, (i * w + w, j * w),
                                 (i * w, j * w + w), 5)
            if board[i][j] == "O":
                pygame.draw.circle(
                    screen, ORANGE, (i * w + w//2, j * w + w//2), w//2, 5)

    return game_obj


def finishedGame(board):
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                return False
    return True


def checkWinner(board):
    n = len(board)
    winner = None

    for i in range(n):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
            winner = board[i][0]

    for i in range(n):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
            winner = board[0][i]

    if board[2][2] == board[1][1] == board[0][0] and board[0][0] != "":
        winner = board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[2][0] != "":
        winner = board[0][2]

    if winner != None:
        return winner
    else:
        if (finishedGame(board)):
            return 'tie'
        return False

def ai_move(board, players, ai):
    n = len(board)
    available = []
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                available.append((i, j))

    # row, col = random.choice(available)

    bestScore = float('-inf')
    bestMove = 0, 0

    for move in available:
        i, j = move
        board[i][j] = players[ai]
        nextPlayer = (ai + 1) % 2
        value = minimax(board, 0, players, nextPlayer)
        board[i][j] = ""
        if (value > bestScore):
            bestScore = value
            bestMove = move

    row, col = bestMove

    board[row][col] = players[ai]


def minimax(board, depth, players, player):

    result = checkWinner(board)
    if (result != False):
        if (result == 'X'):
            return -1
        elif (result == 'O'):
            return 1
        else:
            return 0
    
    else:

        n = len(board)

        if (player == 1):
            maximizeValue = float('-inf')

            for i in range(n):
                for j in range(n):
                    if (board[i][j] != ""):
                        continue
                    board[i][j] = players[player]
                    nextPlayer = (player + 1) % len(players)
                    staticEval = minimax(board, depth, players, nextPlayer)
                    maximizeValue = max(maximizeValue, staticEval)
                    board[i][j] = ""

            return maximizeValue

        if (player == 0):
            minimizeValue = float('inf')

            for i in range(n):
                for j in range(n):
                    if (board[i][j] != ""):
                        continue
                    board[i][j] = players[player]
                    nextPlayer = (player + 1) % len(players)
                    staticEval = minimax(board, depth, players, nextPlayer)
                    minimizeValue = min(minimizeValue, staticEval)
                    board[i][j] = ""
                    
            return minimizeValue


def main():

    n = 3
    w = 80
    running = True
    board = [["" for i in range(n)] for j in range(n)]

    players = ['X', 'O']
    current_player = random.randint(0, 1)

    ai = 1
    if ai == current_player:
        print('AI go first')
    else:
        print('Human go first')

    game_obj = []
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_player != ai:

            for obj in game_obj:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if obj.collidepoint(event.pos):
                        i = obj.x // 80
                        j = obj.y // 80
                        if board[i][j] == "":
                            board[i][j] = players[current_player]
                            current_player = (current_player + 1) % len(players)
        else:
            ai_move(board, players, ai)
            current_player = (current_player + 1) % len(players)

        game_obj = draw_board(n, w, board)

        pygame.display.update()

        pygame.display.flip()

        if checkWinner(board):

            if (checkWinner(board) != 'tie'):

                green = (0, 255, 0)
                blue = (0, 0, 128)
                font = pygame.font.SysFont('Corbel', 35)

                text = font.render(
                    f'{checkWinner(board)} has win the game', True, green, blue)
                screen.blit(text, (400, 300))
                pygame.display.update()

                pygame.time.wait(2000)
                running = False
            else:
                green = (0, 255, 0)
                blue = (0, 0, 128)
                font = pygame.font.SysFont('Corbel', 35)
                text = font.render(
                    'Tie', True, green, blue)
                screen.blit(text, (400, 300))

                pygame.display.update()

                pygame.time.wait(2000)
                running = False

        clock.tick(30)

        screen.fill(BLACK)


main()

# n = 3
# w = 80
# running = True
# board = [["" for i in range(n)] for j in range(n)]

# players = ['X', 'O']
# current_player = random.randint(0, 1)

# ai = random.randint(0, 1)
# if ai == current_player:
#     print('AI go first')
# else:
#     print('Human go first')

# print(board)
# # print(current_player)
# print(minimax(board, 0, players, 0))
# ai_move(board, 0, players, 0)
