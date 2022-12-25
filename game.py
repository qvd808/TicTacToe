import pygame
import random
import numpy as np

pygame.init()

class Display:
    def __init__(self, pygame, width = 800, height = 600) -> None:
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])

        ## Inherit pygame attribute
        self.draw = pygame.draw
        self.display = pygame.display

    def draw_circle(self) -> None:
        self.draw.circle(self.screen, (0, 0, 50, 50), 1)

    def draw_square(self,x, y, width) -> None:
        self.draw.rect(self.screen, 'white', (x, y, width, width),1)
    
    def draw_X(self, i ,j, width):
        self.draw.line(self.screen, "white", (i, j), (i + width, j + width), 5)
        self.draw.line(self.screen, "white", (i + width, j), (i, j + width), 5)


    def draw_board(self, board) -> None: 
        n = board.get_side()
        square_width = board.get_square_width()
        offset_width, offset_height = board.get_offset()

        the_board = board.get_board()

        for i in range(n):
            for j in range(n):
                if (the_board[j][i] != ""):

                    if the_board[j][i] == "X":
                        self.draw_X(square_width * i + offset_width, square_width * j + offset_height, square_width)
                    else:
                    
                        self.draw.circle(self.screen, "white", (square_width * (i + 1/2) + offset_width, square_width * (j + 1/2) + offset_height ), square_width // 2)
                        self.draw.circle(self.screen, (255,220,150), (square_width * (i + 1/2) + offset_width, square_width * (j + 1/2) + offset_height ), square_width // 2, 5)
                
                self.draw_square(square_width * i + offset_width, square_width * j + offset_height, square_width)
    
    def update_display(self) -> None:
        self.display.update()
        self.screen.fill('black')

class Converter:
    def __init__(self) -> None:
        pass
    
    def coordinate_to_index(self, x_Cor, y_Cor, board) -> tuple:
        error_bound = 2 ## This is account for calculating the error when rounding pixel to the index

        square_width = board.get_square_width()
        offset_width, offset_height = board.get_offset()

        i = (x_Cor - offset_width) // (square_width + error_bound)
        j = (y_Cor - offset_height) // (square_width + error_bound)

        return j, i

class Controller:
    def __init__(self) -> None:
        self.converter = Converter()
    
    def is_click_in_range(self, value, off_set, range):
        if value < off_set or value > range - off_set:
            return False
        else:
            return True
    
    def is_board_move(self, x, y, board):
        offset_width, offset_height = board.get_offset()
        width = board.display_width
        height = board.display_height

        if self.is_click_in_range(x, offset_width, width) and self.is_click_in_range(y, offset_height, height):
            return True
        else:
            return False

    def board_move(self, x_Cor, y_Cor, board, player):
        i, j = self.converter.coordinate_to_index(x_Cor, y_Cor, board)
        return board.register_move(i, j, player)
            

class Player:
    def __init__(self, board) -> None:
        self.players = ["X", "O"]
        # self.current_player = random.randint(0, 1)
        # self.ai_player = random.randint(0, 1)
        self.current_player = 1
        self.ai_player = 0

        self.board = board
    
    def player_move(self) -> None:

        try:

            all_move = self.board.get_possible_move()
            best_move = None
            # best_move = random.choice(all_move)
            bestScore = float("-inf")
            for move in all_move:
                i, j = move
                self.board.register_move(i, j, self.players[self.ai_player])
                self.next_player()
                staticValue = self.minimax()
                self.board.erase_move(i, j)
                self.previous_player()
                if (staticValue > bestScore):
                    bestScore = staticValue
                    best_move = move
        
            i, j = best_move


            return i, j
        
        except TypeError:
            print(self.board.get_board())
    
    def get_current_player(self):
        return self.players[self.current_player]
    
    def next_player(self) -> None:
        self.current_player = (self.current_player + 1) % len(self.players)
    
    def previous_player(self) -> None:
        self.current_player = (self.current_player - 1) % len(self.players)

    def minimax(self, alpha = float("-inf"), beta = float("inf"), depth = 0):

        winner = self.board.is_finished()
        depth += 1
        if (winner) or depth == 10:
            if winner == self.players[self.ai_player]:
                return 1
            elif winner == self.players[((self.ai_player + 1) % 2)]:
                return -1
            else:
                return 0
        else:
            if self.current_player == self.ai_player:

                all_move = self.board.get_possible_move()
                maximizeScore = float("-inf")
                for move in all_move:
                    i, j = move
                    self.board.register_move(i, j, self.players[self.ai_player])
                    self.next_player()
                    staticEval = self.minimax(alpha, beta, depth)
                    self.board.erase_move(i, j)
                    self.previous_player()
                    maximizeScore = max(maximizeScore, staticEval)
                    alpha = max(alpha, staticEval)
                    if beta <= alpha:
                        break
                
                return maximizeScore

            if self.current_player != self.ai_player:
                all_move = self.board.get_possible_move()
                minimizeScore = float("inf")
                for move in all_move:
                    i, j = move
                    self.board.register_move(i, j, self.players[(self.ai_player + 1) % 2])
                    self.next_player()
                    staticEval = self.minimax(alpha, beta, depth)
                    self.board.erase_move(i, j)
                    self.previous_player()
                    minimizeScore = min(minimizeScore, staticEval)
                    beta = min(beta, staticEval)
                    if (alpha >= beta):
                        break
                
            return minimizeScore


    def is_ai_player(self):
        if self.current_player == self.ai_player:
            return True
        else:
            return False

class Board:
    def __init__(self, n, display_width, display_height) -> None:
        self.board = [["" for i in range(n)] for j in range(n)]
        self.square_width = 60
        self.width = self.square_width * n

        self.display_width = display_width
        self.display_height = display_height
        self.n = n
    
    def get_board(self):
        return self.board

    def get_square_width(self):
        return self.square_width

    def get_offset(self):
        offset_width = (self.display_width - self.width) // 2
        offset_height = (self.display_height - self.width) // 2

        return (offset_width, offset_height)
    
    def get_side(self):
        return self.n
    
    def register_move(self, i, j, move)  -> bool:
        if self.board[i][j] == "":
            self.board[i][j] = move
            return True
        return False
    
    def erase_move(self, i, j) -> None:
        self.board[i][j] = ""
    
    def get_possible_move(self) -> list:
        all_move = []

        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == "":
                    all_move.append((i, j))

        return all_move

    def is_finished(self):
        board = self.board

        win, player = self.is_winning()
        if win:
            return player

        for i in range(self.n):
            for j in range(self.n):
                if board[i][j] == "":
                    return False

        return True
    
    def is_winning(self):
        streak = 0
        board = self.board

        if 3 <= self.n <= 5:
            streak = 3
        elif 6 <= self.n <= 9:
            streak = 4
        else:
            streak = 5

        ## Check horizontal
        for i in range(self.n):
            j = 0
            end = streak
            while (end != self.n + 1):
                sub_array = board[i][j:end]
                value = set(sub_array)
                if sub_array[0] != "" and len(value) == 1:
                    return True, sub_array[0]
                else:
                    j += 1
                    end += 1
        ## Check vertical
        for i in range(self.n):
            j = 0
            end = streak
            while (end != self.n + 1):
                sub_array = np.array(board)[j:end, i]
                value = set(sub_array)
                if sub_array[0] != "" and len(value) == 1:
                    return True, sub_array[0]
                else:
                    j += 1
                    end += 1
        ## check diaganol
        start = self.n // 2

        diag_list = [np.array(board).diagonal(i) for i in range(-start, start + 1)]
        diag_list.extend(np.array(board)[::-1,:].diagonal(i) for i in range(start + 1, -start - 1, -1))

        for diag in diag_list:
            if len(diag) == streak and diag[0] != "" and len(set(diag)) == 1:
                return True, diag[0]
            elif len(diag) > streak:
                j = 0
                end = streak
                while (end != self.n + 1):
                    sub_array = diag[j:end]
                    value = set(sub_array)
                    if sub_array[0] != "" and len(value) == 1:
                        return True, sub_array[0]
                    else:
                        j += 1
                        end += 1            
        
        return False, None

class Game:
    def __init__(self, n) -> None:
        self.running = True
        self.display = Display(pygame)

        self.n = n
        self.board = Board(n, self.display.width, self.display.height)
        self.controller = Controller()

        self.player = Player(self.board) 

    def quit_handling(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.player.is_ai_player():
                self.register_move(event.pos)
    
    def register_move(self, pos):
        x_Cor, y_Cor = pos
        ## Check if the click is in board and convert the click to board coordinate
        if self.controller.is_board_move(x_Cor, y_Cor, self.board):
            current_player = self.player.get_current_player()
            if (self.controller.board_move(x_Cor, y_Cor, self.board, current_player)):
                self.player.next_player()

    def main_loop(self) -> None:

        while self.running:

            board = self.board.get_board()
            print(board)

            self.quit_handling()

            self.display.draw_board(self.board)

            winner = self.board.is_finished()
            if winner:
                if winner == True:
                    print("Game finished in draw")
                else:
                    print(f"Player {winner} win")
                

                ## Handle if the player want to continue to play
                self.running = False
            
            if self.player.is_ai_player():
                player = self.player.get_current_player()
                i, j = self.player.player_move()
                self.board.register_move(i, j, player)
                self.player.next_player()
                

            self.display.update_display()
