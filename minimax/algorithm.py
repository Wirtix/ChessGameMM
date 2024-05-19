from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255,255,255)

# minimax alghoritm with alpha beta optimalization
def minimax(position, depth, max_player, game,alpha, beta):
    if depth == 0 or position.winner() != None:
        return position.evaluate(max_player), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha,maxEval)
            if beta <= alpha:
                break
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move

    else:
        minEval = float('+inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth - 1, True, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, minEval)
            if beta <= alpha:
                break
            if  minEval == evaluation:
                best_move = move

        return minEval, best_move



def simulate_move(piece, move,board,skip):
    x = board.get_piece(move[0],move[1])
    if x != 0:
        board.remove(x)
    board.move(piece, move[0],move[1])

    return board

def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #draw_moves(game,board,piece) # was used to debug and visualise how alghoritm works
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board,skip)
            moves.append(new_board)

    return moves

# this function is used to show how our model works in real time. used for debugging
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255, 0) , (piece.x, piece.y),50,5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()