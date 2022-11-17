class ScorePolicy():
    def __init__(self) -> None:
        pass

    def finishedGame(self, board):
        n = len(board)
        for i in range(n):
            for j in range(n):
                if board[i][j] == "":
                    return False
        return True

    def checkWinnerBoard(self, board, players):
        winner = None

        for player in players:
            # check row
            for i in range(3):
                if board[i][0] == board[i][1] == board[i][2] == player:
                    return player

            for i in range(3):
                if board[0][i] == board[1][i] == board[2][i] == player:
                    return player

            if board[0][0] == board[1][1] == board[2][2] == player:
                return player

            if board[0][2] == board[1][1] == board[2][0] == player:
                return player
        
        if self.finishedGame(board):
            return "Tie"
        else:
            return winner
        

class MiniMax:
    def __init__(self) -> None:
        self.scorePolicy = ScorePolicy()

    def getAvailableMove(self, board):
        available = []
        n = len(board)
        for i in range(n):
            for j in range(n):
                if board[i][j] == "":
                    available.append((i, j))
        return available
    
    def bestMove(self, board, depth, player):
        players = ["X", "O"]
        availableMove = self.getAvailableMove(board)

        bestScore = float('-inf')
        bestMove = None
        for move in availableMove:
            i, j = move
            board[i][j] = players[player]
            nextPlayer = (player + 1) % 2
            staticValue = self.minimax(board, depth, players, nextPlayer)
            board[i][j] = ""
            if (staticValue > bestScore):
                bestScore = staticValue
                bestMove = move

        return bestMove

    def minimax(self, board, depth, players, player):
        result = self.staticEvaluate(board, players)
        if (result != None):
            return result
        else:
            ## Maximize player
            if (player == 1):
                maximizeScore = float('-inf')

                availableMove = self.getAvailableMove(board)
                for move in availableMove:
                    i, j = move
                    board[i][j] = players[player]
                    nextPlayer = (player + 1) % len(players)
                    staticEval = self.minimax(board, depth, players, nextPlayer)
                    board[i][j] = ""
                    maximizeScore = max(staticEval, maximizeScore)

                return maximizeScore

            ## Minimize player
            if (player == 0):
                minimizeScore = float('inf')

                availableMove = self.getAvailableMove(board)
                for move in availableMove:
                    i, j = move
                    board[i][j] = players[player]
                    nextPlayer = (player + 1) % len(players)
                    staticEval = self.minimax(board, depth, players, nextPlayer)
                    board[i][j] = ""
                    minimizeScore = min(staticEval, minimizeScore)

                return minimizeScore



    
    def staticEvaluate(self, board, players):
        winner = self.scorePolicy.checkWinnerBoard(board, players)
        if winner == 'X':
            return -1
        elif winner == "O":
            return 1
        elif winner == "Tie":
            return 0
        else:
            return None