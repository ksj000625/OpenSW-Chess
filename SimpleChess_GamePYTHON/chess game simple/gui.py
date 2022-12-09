import pygame
import chess
import sys
from random import choice
from traceback import format_exc
from sys import stderr
from time import strftime
from copy import deepcopy
import os
import tkinter as tk

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

CLOCK = pygame.time.Clock()
CLOCK_TICK = 15

SQUARE_SIDE = 95
AI_SEARCH_DEPTH = 2

RED_CHECK = (240, 150, 150)
WHITE = (255, 255, 255)
BLUE_LIGHT = (140, 184, 219)
BLUE_DARK = (91,  131, 159)
GRAY_LIGHT = (240, 240, 240)
GRAY_DARK = (200, 200, 200)
CHESSWEBSITE_LIGHT = (212, 202, 190)
CHESSWEBSITE_DARK = (100,  92,  89)
LICHESS_LIGHT = (240, 217, 181)
LICHESS_DARK = (181, 136,  99)
LICHESS_GRAY_LIGHT = (164, 164, 164)
LICHESS_GRAY_DARK = (136, 136, 136)

BOARD_COLORS = [(GRAY_LIGHT, GRAY_DARK),
                (BLUE_LIGHT, BLUE_DARK),
                (WHITE, BLUE_LIGHT),
                (CHESSWEBSITE_LIGHT, CHESSWEBSITE_DARK),
                (LICHESS_LIGHT, LICHESS_DARK),
                (LICHESS_GRAY_LIGHT, LICHESS_GRAY_DARK)]
BOARD_COLOR = choice(BOARD_COLORS)

BLACK_KING = pygame.image.load('images/black_king.png')
BLACK_QUEEN = pygame.image.load('images/black_queen.png')
BLACK_ROOK = pygame.image.load('images/black_rook.png')
BLACK_BISHOP = pygame.image.load('images/black_bishop.png')
BLACK_KNIGHT = pygame.image.load('images/black_knight.png')
BLACK_PAWN = pygame.image.load('images/black_pawn.png')
BLACK_JOKER = pygame.image.load('images/black_joker.png')

WHITE_KING = pygame.image.load('images/white_king.png')
WHITE_QUEEN = pygame.image.load('images/white_queen.png')
WHITE_ROOK = pygame.image.load('images/white_rook.png')
WHITE_BISHOP = pygame.image.load('images/white_bishop.png')
WHITE_KNIGHT = pygame.image.load('images/white_knight.png')
WHITE_PAWN = pygame.image.load('images/white_pawn.png')
WHITE_JOKER = pygame.image.load('images/white_joker.png')

SCREEN = pygame.display.set_mode((8*SQUARE_SIDE, 8*SQUARE_SIDE))
SCREEN_TITLE = 'Chess Game'
pygame.display.set_caption(SCREEN_TITLE)
pygame.display.set_icon(pygame.image.load('images/chess_icon.ico'))


def resize_screen(square_side_len):
    global SQUARE_SIDE
    global SCREEN
    SCREEN = pygame.display.set_mode(
        (8*square_side_len, 8*square_side_len), pygame.RESIZABLE)
    SQUARE_SIDE = square_side_len


def print_empty_board():
    SCREEN.fill(BOARD_COLOR[0])
    paint_dark_squares(BOARD_COLOR[1])


def paint_square(square, square_color):
    col = chess.FILES.index(square[0])
    row = 7-chess.RANKS.index(square[1])
    pygame.draw.rect(SCREEN, square_color, (SQUARE_SIDE*col,
                     SQUARE_SIDE*row, SQUARE_SIDE, SQUARE_SIDE), 0)


def paint_dark_squares(square_color):
    for position in chess.single_gen(chess.DARK_SQUARES):
        paint_square(chess.bb2str(position), square_color)


def get_square_rect(square):
    col = chess.FILES.index(square[0])
    row = 7-chess.RANKS.index(square[1])
    return pygame.Rect((col*SQUARE_SIDE, row*SQUARE_SIDE), (SQUARE_SIDE, SQUARE_SIDE))


def coord2str(position, color=chess.WHITE):
    if color == chess.WHITE:
        file_index = int(position[0]/SQUARE_SIDE)
        rank_index = 7 - int(position[1]/SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]
    if color == chess.BLACK:
        file_index = 7 - int(position[0]/SQUARE_SIDE)
        rank_index = int(position[1]/SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]


def print_board(board, color=chess.WHITE):
    if color == chess.WHITE:
        printed_board = board
    if color == chess.BLACK:
        printed_board = chess.rotate_board(board)

    print_empty_board()

    if chess.is_check(board, chess.WHITE):
        paint_square(chess.bb2str(chess.get_king(
            printed_board, chess.WHITE)), RED_CHECK)
    if chess.is_check(board, chess.BLACK):
        paint_square(chess.bb2str(chess.get_king(
            printed_board, chess.BLACK)), RED_CHECK)

    for position in chess.colored_piece_gen(printed_board, chess.KING, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_KING,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.QUEEN, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_QUEEN,  (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.ROOK, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_ROOK,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.BISHOP, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_BISHOP, (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.KNIGHT, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_KNIGHT, (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.PAWN, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_PAWN,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.JOKER, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_JOKER,  (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))

    for position in chess.colored_piece_gen(printed_board, chess.KING, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_KING,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.QUEEN, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_QUEEN,  (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.ROOK, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_ROOK,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.BISHOP, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_BISHOP, (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.KNIGHT, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_KNIGHT, (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.PAWN, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_PAWN,   (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.JOKER, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_JOKER,  (SQUARE_SIDE,
                    SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))

    pygame.display.flip()


def set_title(title):
    pygame.display.set_caption(title)
    pygame.display.flip()


def make_AI_move(game, color):
    set_title(SCREEN_TITLE + ' - Calculating move...')
    new_game = chess.make_move(game, chess.get_AI_move(game, AI_SEARCH_DEPTH))
    set_title(SCREEN_TITLE)
    print_board(new_game.board, color)
    return new_game


def try_move(game, attempted_move):
    for move in chess.legal_moves(game, game.to_move):
        if move == attempted_move:
            game = chess.make_move(game, move)
    return game


def play_as(game, color):
    run = True
    ongoing = True
    joker = 0

    while run:
        CLOCK.tick(CLOCK_TICK)
        print_board(game.board, color)

        if chess.game_ended(game):
            set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
            ongoing = False
            
        if ongoing and game.to_move == chess.opposing_color(color):
            game = make_AI_move(game, color)
            
        if chess.game_ended(game):
            set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
            ongoing = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                leaving_square = coord2str(event.pos, color)
                   
            if event.type == pygame.MOUSEBUTTONUP:
                arriving_square = coord2str(event.pos, color)
                    
                if ongoing and game.to_move == color:
                    move = (chess.str2bb(leaving_square), chess.str2bb(arriving_square))
                    game = try_move(game, move)
                    print_board(game.board, color)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == 113:
                    run = False
                if event.key == 104 and ongoing: # H key
                    game = make_AI_move(game, color)
                if event.key == 117: # U key
                    game = chess.unmake_move(game)
                    game = chess.unmake_move(game)
                    set_title(SCREEN_TITLE)
                    print_board(game.board, color)
                    ongoing = True
                if event.key == 99: # C key
                    global BOARD_COLOR
                    new_colors = deepcopy(BOARD_COLORS)
                    new_colors.remove(BOARD_COLOR)
                    BOARD_COLOR = choice(new_colors)
                    print_board(game.board, color)
                if event.key == 112 or event.key == 100: # P or D key
                    print(game.get_move_list() + '\n')
                    print('\n'.join(game.position_history))
                if event.key == 101: # E key
                    print('eval = ' + str(chess.evaluate_game(game)/100))
                if event.key == 106: # J key
                    joker += 1
                    if joker == 13 and chess.get_queen(game.board, color):
                        queen_index = chess.bb2index(chess.get_queen(game.board, color))
                        game.board[queen_index] = color|chess.JOKER
                        print_board(game.board, color)
                
            if event.type == pygame.VIDEORESIZE:
                if SCREEN.get_height() != event.h:
                    resize_screen(int(event.h/8.0))
                elif SCREEN.get_width() != event.w:
                    resize_screen(int(event.w/8.0))
                print_board(game.board, color)

    pygame.display.update
    
def play_as_white(game=chess.Game()):
    return play_as(game, chess.WHITE)


def play_as_black(game=chess.Game()):
    return play_as(game, chess.BLACK)


def play_random_color(game=chess.Game()):
    color = choice([chess.WHITE, chess.BLACK])
    play_as(game, color)

# play_as_white()


def get_font(size):
    return pygame.font.SysFont("arial", size, True, True)


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)


def blitz():
    while True:
        BLITZ_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        BLITZ_TEXT = get_font(100).render("BLITZ", True, "#b68f40")
        BLITZ_RECT = BLITZ_TEXT.get_rect(center=(380, 110))
        SCREEN.blit(BLITZ_TEXT, BLITZ_RECT)

        TEXT = get_font(40).render(
            "Blitz chess simply refers to a game of", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.x=90
        TEXT_RECT.y=220
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(40).render(
            "chess that has a fast time control.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.x=120
        TEXT_RECT.y=260
        SCREEN.blit(TEXT, TEXT_RECT)

        TEXT = get_font(40).render(
            "Each player is given 10 minutes or less.", True, "white")
        TEXT_RECT = TEXT.get_rect()
        TEXT_RECT.x=90
        TEXT_RECT.y=320
        SCREEN.blit(TEXT, TEXT_RECT)

        BLITZ_BACK = Button(image=None, pos=(600, 500),
                            text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")
        BLITZ_GAME = Button(image=None, pos=(160, 500),
                            text_input="START", font=get_font(50), base_color="White", hovering_color="Green")

        for button in [BLITZ_GAME, BLITZ_BACK]:
            button.changeColor(BLITZ_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BLITZ_BACK.checkForInput(BLITZ_MOUSE_POS):
                    main_menu()
                if BLITZ_GAME.checkForInput(BLITZ_MOUSE_POS):
                    play_as_white()
        pygame.display.update()

def rules():
    while True:
        CRAZY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")


        RULE_BACK = Button(image=None, pos=(380, 500), 
                            text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")               

        RULE_BACK.changeColor(CRAZY_MOUSE_POS)
        RULE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RULE_BACK.checkForInput(CRAZY_MOUSE_POS):
                    main_menu()
        pygame.display.update()


def main_menu():
    pygame.display.set_caption("CHESS GAME")

    while True:
        SCREEN.fill("black")  
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("CHESS GAME", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(380, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        BLITZ_BUTTON = Button(image=None, pos=(380, 400), 
                            text_input="BLITZ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        RULE_BUTTON = Button(image=None, pos=(380, 300), 
                            text_input="CHESS RULES", font=get_font(75), base_color="gray", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(380, 500), 
                            text_input="QUIT", font=get_font(75), base_color="gray", hovering_color="White")  
        for button in [BLITZ_BUTTON, RULE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BLITZ_BUTTON.checkForInput(MENU_MOUSE_POS):
                    blitz() 
                if RULE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rules() 
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()    
main_menu()    
