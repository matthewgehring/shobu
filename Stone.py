#not in use currently
class Stone:
    def __init__(self, board, x, y, color):
        self.board = board
        self.position = (x,y)
        self.color = color
    
    def update_position(self, x, y):
        self.position = (x,y)
    