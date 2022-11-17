import unittest
from Minimax import MiniMax, ScorePolicy

class MiniMaxTest(unittest.TestCase):

    def createBoard(self, n):
        return [["" for i in range(n)] for j in range(n)]

    def printBoard(self, board):
        n = len(board)
        for i in range(n):
            print(board[i])

    def setUp(self) -> None:
        self.players = ["X", "O"]
        self.scorePolicy = ScorePolicy()
        self.emptyBoard = self.createBoard(3)
        self.tieBoard = [
            ["X", "O", "X"],
            ["X", "O", "O"],
            ["O", "X", "X"],
        ]
        self.tieBoard = [
            ["X", "O", "X"],
            ["X", "O", "O"],
            ["O", "X", "X"],
        ]
        self.XWinBoard = [
            ["X", "", "O"],
            ["X", "O", ""],
            ["X", "", ""],
        ]
        self.OWinBoard = [
            ["O", "O", "O"],
            ["X", "X", ""],
            ["O", "X", ""],
        ]
        self.minimax = MiniMax()

    def test_checkWinner(self):
        result = self.scorePolicy.checkWinnerBoard(self.emptyBoard, self.players)
        self.assertEqual(result, None)

        result = self.scorePolicy.checkWinnerBoard(self.XWinBoard, self.players)
        self.assertEqual(result, self.players[0])

        result = self.scorePolicy.checkWinnerBoard(self.OWinBoard, self.players)
        self.assertEqual(result, self.players[1])

        result = self.scorePolicy.checkWinnerBoard(self.tieBoard, self.players)
        self.assertEqual(result, "Tie")


    def test_eval(self):
        result = self.minimax.staticEvaluate(self.tieBoard, self.players)
        self.assertEqual(result, 0)

        result = self.minimax.staticEvaluate(self.XWinBoard, self.players)
        self.assertEqual(result, -1)

        result = self.minimax.staticEvaluate(self.OWinBoard, self.players)
        self.assertEqual(result, 1)

        result = self.minimax.staticEvaluate(self.emptyBoard, self.players)
        self.assertEqual(result, None)

    def test_BestMove(self):
        # O is playing next turn
        testBoard = [
            ["X", "X", ""],
            ["X", "O", ""],
            ["O", "", ""],
        ]
        bestMove = self.minimax.bestMove(testBoard,0, 1)
        self.assertEqual(bestMove, (0,2))

        # O is playing next turn
        testBoard = [
            ["X", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]
        bestMove = self.minimax.bestMove(testBoard, 0, 1)
        self.assertEqual(bestMove, (1, 1))

if __name__ == "__main__":
    unittest.main()