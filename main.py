# importing
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK,IBG, LGREY
from checkers.game import Game, Button
from pygame import mixer
from minimax.algorithm import minimax

# pygame initialization
pygame.init()

# some constans setting
FPS = 60
tryb = 'ai'
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')
text = pygame.font.Font('intro_font.ttf', 64)
subtext =   pygame.font.Font('intro_font.ttf', 18)
ai_level = 2 # standard ai difficulty

mixer.init()
mixer.music.load('assets/bensound-summer_mp3_music.mp3')

def get_row_col_from_mouse(pos): # returning in which col and row our mouse is now
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# intro function which contains game mode selection
def intro():
    intro = True
    clock = pygame.time.Clock()
    game1 = Game(WIN)
    #defining buttons on intro
    play_button = Button(250, 350, 300, 50, WHITE, BLACK, 'Play with AI', 32)
    easy_button = Button(300, 450, 50, 50, WHITE, BLACK, 'Easy', 20)
    mid_button = Button(370, 450, 50, 50, WHITE, BLACK, 'Mid', 20)
    hard_button = Button(440, 450, 50, 50, WHITE, BLACK, 'Hard', 20)
    single_player_button = Button(250, 290, 300, 50, WHITE, BLACK, 'Single Player', 32)

    #main intro loop
    while intro:
        global ai_level
        global tryb
        title = text.render('CHESS GAME', True, WHITE)
        title_rect = title.get_rect(x=160, y=200)
        options = subtext.render('Choice LEVEL:', True, WHITE)
        options_rect = options.get_rect(x=320, y=420)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # buttons 
        if play_button.is_pressed(mouse_pos, mouse_pressed):
            intro = False
            tryb = 'ai'
            main()
        elif single_player_button.is_pressed(mouse_pos, mouse_pressed):
            intro = False
            tryb = 'single'
            main()
        elif easy_button.is_pressed(mouse_pos, mouse_pressed):
            ai_level = 1
            easy_button.change_color(LGREY)
            mid_button.change_color(BLACK)
            hard_button.change_color(BLACK)
            game1.click_sound(1)
        elif mid_button.is_pressed(mouse_pos, mouse_pressed):
            ai_level = 2
            mid_button.change_color(LGREY)
            easy_button.change_color(BLACK)
            hard_button.change_color(BLACK)
            game1.click_sound(1)
        elif hard_button.is_pressed(mouse_pos, mouse_pressed):
            ai_level = 3
            hard_button.change_color(LGREY)
            easy_button.change_color(BLACK)
            mid_button.change_color(BLACK)
            game1.click_sound(1)


        WIN.blit(IBG,  (0,0))
        WIN.blit(title, title_rect)
        WIN.blit(options, options_rect)
        WIN.blit(play_button.image, play_button.rect)
        WIN.blit(single_player_button.image, single_player_button.rect)
        WIN.blit(easy_button.image, easy_button.rect)
        WIN.blit(mid_button.image, mid_button.rect)
        WIN.blit(hard_button.image, hard_button.rect)
        clock.tick(FPS)
        pygame.display.update()


def main():
    run = True
    #setting constans FPS to avoid speeding game
    clock = pygame.time.Clock()
    game = Game(WIN)

    # turns on music
    mixer.music.play()
    mixer.music.set_volume(0.01)

    # game controlling loop
    while run:
        clock.tick(FPS)
        
        # mini-max algorythm player selection
        if tryb == 'ai':
            if game.turn == WHITE:
                value, new_board = minimax(game.get_board(),ai_level, True, game,float('-inf'), float('+inf'))

                game.ai_move(new_board)
        # checking if game have a winner
        if game.score == True:
            print(f'The winner is :{game.winner()}')
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # We are checking if player did anything with any pawn
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)

                game.select(row,col)

        game.update()


    pygame.quit()

# turning on intro 
intro()