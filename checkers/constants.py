import pygame

'''
Couse of using many constants i decidet to make this file where we have 
most of important things used in other files
'''

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8,8
SQUARE_SIZE = WIDTH // COLS

# Color deff
#RGB    R    G   B
RED = (255, 0 , 0)
WHITE = (255,255 ,255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
LGREY = (192, 192 ,192)
GREEN = (0, 255, 0)

#Here we load phots of our figures
#Black : 

CROWN = pygame.transform.scale(pygame.image.load('assets/queen.svg'), (60,60) )
IBG = pygame.transform.scale(pygame.image.load('assets/background.jpg'), (800,800))
PAWN = pygame.transform.scale(pygame.image.load('assets/pawn.svg'), (300, 300) )
ROOK = pygame.transform.scale(pygame.image.load('assets/rook.svg'), (300, 300) )
KNIGHT = pygame.transform.scale(pygame.image.load('assets/knight.svg'), (300, 300) )
BISHOP = pygame.transform.scale(pygame.image.load('assets/bishop.svg'), (300, 300) )
QUEEN = pygame.transform.scale(pygame.image.load('assets/queen.svg'), (300, 300) )
KING = pygame.transform.scale(pygame.image.load('assets/king.svg'), (300, 300) )

#WHITE:
WPAWN = pygame.transform.scale(pygame.image.load('assets/white/pawn.svg'), (300, 300) )
WROOK = pygame.transform.scale(pygame.image.load('assets/white/rook.svg'), (300, 300) )
WKNIGHT = pygame.transform.scale(pygame.image.load('assets/white/knight.svg'), (300, 300) )
WBISHOP = pygame.transform.scale(pygame.image.load('assets/white/bishop.svg'), (300, 300) )
WQUEEN = pygame.transform.scale(pygame.image.load('assets/white/queen.svg'), (300, 300) )
WKING = pygame.transform.scale(pygame.image.load('assets/white/king.svg'), (300, 300) )
