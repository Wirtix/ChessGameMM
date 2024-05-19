
from .constants import SQUARE_SIZE, KNIGHT, ROOK, BISHOP, QUEEN, KING, PAWN, RED, WHITE, WKNIGHT, WROOK, WBISHOP, WQUEEN, WKING, WPAWN


'''
This file contains properties of every figure so we can use it later.
'''
class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.type = 'Piece'
        self.king = False



        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        #pu oureself on middle of place
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_queen(self): # like in real chess. if piece is in oposide last row then u become queen
        self.king = True


    def draw(self, win, z=0):
        if self.king:
            if self.color == RED:
                win.blit(QUEEN, (self.x - 40, self.y - 40))
            elif self.color == WHITE:
                win.blit(WQUEEN, (self.x - 40, self.y - 40))
        else:
            if self.color == RED:
                win.blit(PAWN, (self.x - 40, self.y - 40))
            elif self.color == WHITE:
                win.blit(WPAWN, (self.x - 40, self.y - 40))

    def move(self,row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
# all classes inherit from Pieces class
class Knight(Piece):   
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.type = 'Knight'
    def draw(self, win, z=0):
        if self.color == RED:
            win.blit(KNIGHT, (self.x - 40, self.y - 40))
        if self.color == WHITE:
            win.blit(WKNIGHT, (self.x - 40, self.y - 40))


class Rook(Piece):         
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.type = 'Rook'

    def draw(self, win, z=0):
        if self.color == RED:
            win.blit(ROOK,  (self.x - 40, self.y - 40))
        else:
            win.blit(WROOK, (self.x - 40, self.y - 40))
class Bishop(Piece):    #goniec
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.type = 'Bishop'

    def draw(self, win, z=0):
        if self.color == RED:
            win.blit(BISHOP, (self.x - 40, self.y - 40))
        else:
            win.blit(WBISHOP, (self.x - 40, self.y - 40))

class King(Piece):    #Król
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.type = 'King'
    def draw(self, win, z=0):
        if self.color == RED:
            win.blit(KING, (self.x - 40, self.y - 40))
        else:
            win.blit(WKING, (self.x - 40, self.y - 40))

class Queen(Piece):    #Królowa
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.type = 'Queen'

    def draw(self, win, z=0):
        if self.color == RED:
            win.blit(QUEEN, (self.x - 40, self.y - 40))
        else:
            win.blit(WQUEEN, (self.x - 40, self.y - 40))