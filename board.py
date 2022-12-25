

from game import Drawer

class Board:
    def __init__(self, width: int, drawer: Drawer) -> None:
        self.width = width
        self.drawer = drawer
        self.board = [["" for i in range(width)] for j in range(width)]
    
    def draw() -> None:
        pass