import pygame
from .constants import ROWS, RED, SQUARE_SIZE, COLS, WHITE, LGREY, BLACK
from .piece import Piece, Rook, Knight, King, Queen, Bishop



'''Here we have everythink about board. 
I decided to build chess as continuation of checkers game so I used raw pygames
without chess library. no moves like E2 to E3. Just moving for squares 
in our printed board

'''

class Board:


    def __init__(self): 
        self.board = []
        self.create_board()
        self.checkrow = -1
        self.checkcol = -1
        self.score = False
        self.castling = True

        #list of avaliable figures
        self.red_left = self.white_left = 16
        self.white_queen = self.red_queen = 1
        self.white_king = self.red_king = 1
        self.white_krb = self.red_krb = 6
        self.white_piece = self.red_piece = 8


    def evaluate(self, max_player):
        self.white_score = self.white_piece*10 + self.white_king * 10000 + self.white_krb * 50 + self.white_queen * 90

        self.red_score = self.red_piece*10 + self.red_king * 10000 + self.red_krb * 50 + self.red_queen * 90

        if max_player:
            x = self.white_score - self.red_score
        else:
            x = self.red_score - self.white_score


        return x

    def get_all_pieces(self,color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces



    def move(self, piece, row, col):
        if piece != 0:
            self.board[piece.row][piece.col], self.board[row][col] =  self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row,col)
            if piece != 0 :
                if (row == ROWS-1 or row == 0) and piece.type == 'Piece':
                    piece.make_queen()
                    if piece.color == WHITE:
                        self.white_queen += 1
                    else:
                        self.red_queen += 1
                if piece.type == 'Rook' or piece.type == 'King':
                    self.castling = False
    def get_piece(self, row, col):
        return self.board[row][col]
    def get_king(self):
        king_list = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece != 0:
                    type = piece.type
                    if piece.type == 'King':
                        king_list.append((self.get_piece(row,col).row,self.get_piece(row,col).col))


        return king_list

    def draw_squares(self,win):
        win.fill(BLACK)
        for row in range(ROWS):
            #drukujemy czerwone pola na czarnych z offsetem
            for col in range(row % 2,ROWS,2):
                pygame.draw.rect(win, LGREY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Here we create our visible part of board
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                #piece
                if row == 1 :
                    self.board[row].append(Piece(row, col, WHITE))
                elif row == 6:
                    self.board[row].append(Piece(row, col, RED))
                #rook
                elif row == 0 and (col ==0  or col == 7):
                    self.board[row].append(Rook(row, col, WHITE))
                elif row == 7 and (col == 0 or col == 7):
                    self.board[row].append(Rook(row, col, RED))
                #Knight
                elif row == 0 and (col == 1 or col == 6):
                    self.board[row].append(Knight(row, col, WHITE))
                elif row == 7 and (col == 1 or col == 6):
                    self.board[row].append(Knight(row, col, RED))
                #bishoop
                elif row == 0 and (col == 2 or col == 5):
                    self.board[row].append(Bishop(row, col, WHITE))
                elif row == 7 and (col == 2 or col == 5):
                    self.board[row].append(Bishop(row, col, RED))
                #Queen
                elif row == 0 and (col == 3 ):
                    self.board[row].append(Queen(row, col, WHITE))
                elif row == 7 and (col == 3 ):
                    self.board[row].append(Queen(row, col, RED))
                #King
                elif row == 0 and (col == 4 ):
                    self.board[row].append(King(row, col, WHITE))
                elif row == 7 and (col == 4 ):
                    self.board[row].append(King(row, col, RED))

                else:
                    self.board[row].append(0)
            else:
                self.board[row].append(0)
    def draw(self, win):
        self.draw_squares(win)
        self.draw_check(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    #adaptacja wcisnietego przycisku


    # removes captured pieces
    def remove(self,pieces):
        if pieces.type == 'King':
            if pieces.color == WHITE:
                self.white_king = 0
            else:
                self.red_king = 0
        elif pieces.type == 'Piece':
            if pieces.color == WHITE:
                self.white_piece -= 1
            else:
                self.red_piece -= 1
        elif pieces.type == 'Queen':
            if pieces.color == WHITE:
                self.white_queen -= 1
            else:
                self.red_queen -= 1
        else:
            if pieces.color == WHITE:
                self.white_krb -=1
            else:
                self.red_krb -= 1
        self.board[pieces.row][pieces.col] = 0


        if pieces != 0:
            if pieces.color == RED:
                self.red_left -=1
            else:
                self.white_left -=1
    #diffrent ways to check if there is mat
    def winner(self):
        if self.red_king <=0:
            print('R is badd')
            return WHITE
        elif self.white_king <=0:
            print('B is badd')
            return RED
        else:
            return None
    def check_mat(self, color):
        self.score = True
        if color == WHITE:
            print('RED SSIE')
            return WHITE, self.score
        elif color == RED:
            print('BIAŁY SSIE')
            return RED, self.score




#algorytm sprawdzający możliwe ruchy:

    def check(self):
        king_list = self.get_king()
        all_valid_moves = []
        if len(king_list) < 2:
            if self.red_king == 0: self.check_mat(WHITE)
            else:  self.check_mat(RED)
        else:
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.get_piece(row,col)
                    if piece != 0:
                        all_valid_moves.append(self.get_valid_moves(piece))
            for item in all_valid_moves:
                if king_list[0] in item.keys():
                    print('CRITICAL MOMENT OMG')
                    self.checkrow = king_list[0][1]
                    self.checkcol = king_list[0][0]
                    break
                elif king_list[1] in item.keys():
                    print('CRITICAL MOMENT OMG')
                    self.checkrow = king_list[1][1]
                    self.checkcol = king_list[1][0]
                    break
                else:
                    self.checkcol = -1
                    self.checkrow = -1

    # drawing if dangerous situation
    def draw_check(self,win):
        if self.checkrow != -1:
            pygame.draw.rect(win, RED, (self.checkrow * SQUARE_SIZE, self.checkcol * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def castling_move(self, start, color, front):
        print('castling')
        moves = {}
        if color == WHITE:
                moves[(start,front + 3)] = self.board[start][front + 3]
                moves[(start, front - 4)] = self.board[start][front - 4]
        else:
                moves[(start, front + 3)] = self.board[start][front + 3]
                moves[(start, front - 4)] = self.board[start][front - 4]

        return moves


    # look for valid moves and create dict with valid moves
    def get_valid_moves(self, piece):
        moves = {}
        type = piece.type
        front = piece.col
        row = piece.row

        # białe ida w dół więc dodajemy a czerwone do góry
        if type == 'Piece' and not piece.king:
            if piece.color == RED or piece.king:
                moves.update(self.pionek_traverse_forward(row, piece.color, front))
            if piece.color == WHITE or piece.king:
                moves.update(self.pionek_traverse_forward(row, piece.color, front))
        if type == 'Rook':
             if piece.color == RED or piece.king:
                 moves.update(self.rook_traverse_forward(row, piece.color, front))
             if piece.color == WHITE or piece.king:
                 moves.update(self.rook_traverse_forward(row, piece.color, front))

        if type == 'Knight':
             if piece.color == RED or piece.king:
                 moves.update(self.knight_traverse_forward(row, piece.color, front))
             if piece.color == WHITE or piece.king:
                 moves.update(self.knight_traverse_forward(row, piece.color, front))

        if type == 'Bishop':
             if piece.color == RED or piece.king:
                 moves.update(self.bishop_traverse_forward(row, piece.color, front))
             if piece.color == WHITE or piece.king:
                 moves.update(self.bishop_traverse_forward(row, piece.color, front))

        # used connection bishop with rook
        if type == 'Queen' or piece.king :
             if piece.color == RED or piece.king:
                 moves.update(self.rook_traverse_forward(row, piece.color, front))
                 moves.update(self.bishop_traverse_forward(row, piece.color, front))
             if piece.color == WHITE or piece.king:
                 moves.update(self.rook_traverse_forward(row, piece.color, front))
                 moves.update(self.bishop_traverse_forward(row, piece.color, front))
        if type == 'King':
             if piece.color == RED or piece.king:
                 moves.update(self.king_traverse_forward(row, piece.color, front))
                 #if self.castling:
                     #pass
                     #moves.update(self.castling_move(row, piece.color, front))
             if piece.color == WHITE or piece.king:
                moves.update(self.king_traverse_forward(row, piece.color, front))
                #if self.castling:
                    #pass
                    #moves.update(self.castling_move(row, piece.color, front))


        return moves
    
    # Here we have big section with every single move deffinition. Place to improve
    def pionek_traverse_forward(self, start, color, front):
        moves = {}

        if color == WHITE:
            if start == 1:
                z = 2
            else:
                z = 1
            right = self.board[start + 1][front+1]
            left = self.board[start + 1][front - 1]
            for r in range(start, start+z, 1):
                if start < 8:
                    current = self.board[r+1][front]
                    if current == 0:
                        moves[(r+1,front)] = current
                    else:
                        break
            if right != 0 and right.color != color:
                moves[(start+1,front+1)] = right

            if left != 0 and left.color != color:
                moves[(start + 1,front - 1)] = left

        elif color == RED:
            if start == 6:
                z = 2
            else:
                z = 1

            right = self.board[start - 1][front + 1]
            left = self.board[start - 1][front - 1]
            for r in range(start, start -z, -1):
                current = self.board[r-1][front]
                if current == 0:
                    moves[(r - 1, front)] = current
                else:
                    break
            if right != 0 and right.color != color:
                moves[(start - 1,front + 1)] = right
            if left != 0 and left.color != color:
                moves[(start - 1,front - 1)] = left
        return moves

    def rook_traverse_forward(self, start, color, front):
        moves = {}
        # move down
        for r in range(start+1, 8, 1):
            forward  = self.board[r][front]
            if forward == 0:
                moves[(r,front)] = forward
            elif forward != 0 and forward.color != color:
                moves[(r,front)] = forward
                break
            else :
                break
        # move up
        for r in range(start-1, -1, -1):
            if start > -1 :
                forward = self.board[r][front]

                if forward == 0:
                    moves[(r, front)] = forward
                elif forward != 0 and forward.color != color:
                    moves[(r, front)] = forward
                    break
                else :
                    break
        # left
        for r in range(front-1, -1, -1):
            left = self.board[start][r]

            if left == 0:
                moves[(start, r)] = left
            elif left != 0 and left.color != color:
                moves[(start, r)] = left
                break
            else :
                break
        # right
        for r in range(front + 1, 8, 1):
            left = self.board[start][r]

            if left == 0:
                moves[(start, r)] = left
            elif left != 0 and left.color != color:
                moves[(start, r)] = left
                break
            else:
                break



        return moves


    def knight_traverse_forward(self, start, color, front):
        moves = {}

        if start < 6:
            fright = self.board[start + 2][front + 1]
            xfright = (start + 2, front + 1)
            fleft = self.board[start + 2][front - 1]
            xfleft = (start + 2, front - 1)
            if fright == 0 or (fright != 0 and fright.color != color):
                moves[xfright] = fright
            if fleft == 0 or (fleft != 0 and fleft.color != color):
                moves[xfleft] = fleft
        if start < 7:
            ltop = self.board[start + 1][front - 2]
            xltop = (start + 1, front - 2)
            if ltop == 0 or (ltop != 0 and ltop.color != color):
                moves[xltop] = ltop
        if start > 1:
            dright = self.board[start - 2][front + 1]
            xdright = (start - 2, front + 1)
            dleft = self.board[start - 2][front - 1]
            xdleft = (start - 2, front - 1)
            lbot = self.board[start - 1][front - 2]
            xlbot = (start - 1, front - 2)
            if dright == 0 or (dright != 0 and dright.color != color):
                moves[xdright] = dright
            if dleft == 0 or (dleft != 0 and dleft.color != color):
                moves[xdleft] = dleft
            if lbot == 0 or (lbot != 0 and lbot.color != color):
                moves[xlbot] = lbot

        if start < 7 and start > 0:
            if front < 7:
                rtop = self.board[start + 1][front + 2]
                xrtop = (start + 1, front + 2)
                rbot = self.board[start - 1][front + 2]
                xrbot = (start - 1, front + 2)
                if rtop == 0 or (rtop != 0 and rtop.color != color):
                    moves[xrtop] = rtop
                if rbot == 0 or (rbot != 0 and rbot.color != color):
                    moves[xrbot] = rbot


        return moves

    def bishop_traverse_forward(self, start, color, front):
        moves = {}
        x = 1
        if color == WHITE or (color == RED and start < 7):
            for r in range(start+1, 8 , 1):

                if x + front < 9 :
                    right = self.board[r][front + x]
                    if right == 0 :
                        moves[(r,front+x)] = right
                    elif right!= 0 and right.color !=color:
                        moves[(r, front + x)] = right
                        break
                    elif (right != 0 and right.color == color):
                        break

                x +=1
            x = 1
            for r in range(start+1, 8, 1):
                if front - x > -1:
                    left = self.board[r][front - x]

                    if left == 0:
                        moves[(r,front-x)] = left
                    elif left != 0 and left.color != color:
                        moves[(r, front - x)] = left
                        break
                    elif (left != 0 and left.color == color):
                        break

                x += 1

        x = 1
        if color == RED or (color == WHITE and start > 0):
            for r in range(start-1, -1 , -1):

                if x + front < 9:
                    right = self.board[r][front + x]
                    if (right != 0 and right.color == color):
                        break
                    elif right == 0  :
                        moves[(r,front+x)] = right
                    elif  right!= 0 and right.color !=color:
                        moves[(r, front + x)] = right
                        break
                x += 1
            x=1
            for r in range(start - 1, -1, -1):
                if (front - x) > -1:
                    left = self.board[r][front - x]
                    if left == 0:
                        moves[(r,front-x)] = left
                    elif left!= 0 and left.color !=color:
                        moves[(r, front - x)] = left
                        break
                    elif (left != 0 and left.color == color):
                        break

                x += 1
        return moves

    def king_traverse_forward(self, start, color, front):
        moves = {}

        if start  < 7 :
            forward = self.board[start + 1][front]

            if forward == 0 or (forward != 0 and forward.color != color):
                moves[(start + 1, front)] = forward

            if front > 0 and front < 7:
                fright = self.board[start + 1][front + 1]
                fleft = self.board[start + 1][front - 1]
                if fright == 0 or (fright != 0 and fright.color != color):
                    moves[(start + 1, front + 1)] = fright
                if fleft == 0 or (fleft != 0 and fleft.color != color):
                    moves[(start + 1, front - 1)] = fleft

        if start > 0:
            back = self.board[start - 1][front]

            if back == 0 or (back != 0  and back.color != color):
                moves[(start - 1, front)] = back
            if front > 0 and front < 7:
                bright = self.board[start - 1][front + 1]
                bleft = self.board[start - 1][front - 1]
                if bright == 0 or (bright != 0 and bright.color != color):
                    moves[(start - 1, front + 1)] = bright
                if bleft == 0 or (bleft != 0 and bleft.color != color):
                    moves[(start - 1, front - 1)] = bleft

        if front > 0 and front < 7:
            right = self.board[start][front + 1]
            left = self.board[start][front - 1]
            if right == 0 or (right != 0 and right.color != color):
                moves[(start, front+1)] = right
            if left == 0 or (left != 0 and left.color !=color):
                moves[(start, front -1)] = left

        return moves
