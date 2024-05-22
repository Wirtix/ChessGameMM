import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board
from pygame import mixer


class Game:

    def __init__(self, win):
        self._init()
        self.win = win
        self.scol = []
        self.srow = []
        self.cords = ()
        self.score = False

    def update(self):   
        self.board.draw(self.win)
        # we are drawing 
        self.draw_valid_moves(self.valid_moves)
        self.draw_clicked(self.win, self.cords)
        self.score = self.board.score
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col): # we select some piece and then show it valid moves
        self.cords = (0, 0)
        self.cords = (row, col)
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:

            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            self.board.check()
            return True

        return False

    def click_sound(self, x=0): # sound of clicking pieces
        mixer.init()
        if x == 1:
            sound1 = pygame.mixer.Sound("assets/click_sound.wav")
        else:
            sound1 = pygame.mixer.Sound("assets/skipped.wav")

        pygame.mixer.find_channel().play(sound1)
        mixer.music.set_volume(0.1)

    def _move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            skipped = self.valid_moves[(row, col)]
            x = 1
            if skipped:
                self.board.remove(skipped)
                x = 0

            self.board.move(self.selected, row, col)
            self.click_sound(x)
            self.change_turn()
        else:
            return False

        return True

    def winner(self):
        return self.board.winner()
    def draw_valid_moves(self,moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE+SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2),10)


    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
            return self.board

    def ai_move(self,board):
        self.click_sound(1)
        self.board = board
        self.change_turn()
    def draw_clicked(self, win, piece):
        if piece :
            x, y = piece
            radius = SQUARE_SIZE // 2 - 40
            pygame.draw.circle(win, (255,128,128), (y*SQUARE_SIZE+SQUARE_SIZE//2, x*SQUARE_SIZE+SQUARE_SIZE//2), radius - 2)
class Button:
    def __init__(self, x,y ,width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('intro_font.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center =(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self,pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    def change_color(self, color):
        self.bg = color
        self.image.fill(self.bg)
        self.image.blit(self.text, self.text_rect)
        pygame.display.update()




