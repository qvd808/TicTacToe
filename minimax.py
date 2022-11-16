board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""],
]

players = ['X', 'O']
ai = 1

def gameFinished(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                return False
    return True

def checkWinner(board):

    for player in players:

        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == player:
                return player

        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] == player:
                return player
        
        if board[2][2] == board[1][1] == board[0][0] == player:
            return player

        if board[0][2] == board[1][1] == board[2][0] == player:
            return player
    
    if gameFinished(board):
        return 'Tie'
    
    return None

def ai_move(board):
    available = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                available.append((i, j))
    
    bestScore = float('-inf')
    bestMove = None
    for move in available:
        i, j = move
        result = minimax(board, 0, ai)
        if (result > bestScore):
            bestScore = result
            bestMove

def draw_board(board):
    print(board[0])
    print(board[1])
    print(board[2])


def minimax(board, depth, player):
    result = checkWinner(board)
    if result == 'X':
        return -1
    elif result == 'O':
        return 1
    elif result == "tie":
        return 0
    else:

        return 1


draw_board(board)
ai_move(board)
# value = minimax(board, 0, player=ai)
# print(value)
