from glob import glob
from multiprocessing import connection
from re import T
from shutil import move
from turtle import pos
import pygame
import os
from GameFramework import *
from Draughts import *
from AIPlayers import *


#pygame init
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 800, 400
pygame.display.set_caption("Draughts with AI")
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
HEALTH_FONT = pygame.font.SysFont('comicsans', 12)
TUTOR_FONT = pygame.font.SysFont('comicsans', 24)
OVER_FONT = pygame.font.SysFont('comicsans', 24)

#game init
WHITE = (240, 240, 240)
BOARD=(230,230,230)
BLACK = (39, 39, 39)
PLAYER2_COLOR=(39, 39, 39)
RED = (154, 34, 20)
PLAYER1_COLOR=(154, 34, 20)
YELLOW = (255, 255, 0)
GREY=(90,90,90)
SQUARE_SIZE=50
PIECE_RADIUS=50
ROUND=6

BKImg = pygame.image.load(os.path.join("Assets","BK.png"))
BK=pygame.transform.scale(BKImg,(SQUARE_SIZE,SQUARE_SIZE))

RKImg = pygame.image.load(os.path.join("Assets","RK.png"))
RK=pygame.transform.scale(RKImg,(SQUARE_SIZE,SQUARE_SIZE))

BMImg = pygame.image.load(os.path.join("Assets","BM.png"))
BM=pygame.transform.scale(BMImg,(SQUARE_SIZE,SQUARE_SIZE))

RMImg = pygame.image.load(os.path.join("Assets","RM.png"))
RM=pygame.transform.scale(RMImg,(SQUARE_SIZE,SQUARE_SIZE))


#game utils
def location(x):
    return  x*SQUARE_SIZE

def piece_location(x):
    return x*PIECE_RADIUS+PIECE_RADIUS/2

KING_SIZE=4
WHITE_SQUARE=pygame.Rect(0,0,50,50)
PIECES_DICT={}



class PIECE:
    def __init__(self):
        self.pos=()
        self.player=-1
        self.surface=None
        self.isKing=False
        self.isFocus=False
        self.gird_pos=()
        self.move_grid_pos=[]
        #for next select
        self.move_tips_pieces=[]

FOCUS_PIECE_GRID_POS=()

def update_draw(game,player):
    WIN.fill(BOARD)
    if game.isOver:
        #TODO
        #wrong player name due to wrong game round
        if game.winner == 0:
            winner="DRAW"
        else:
            winner=player.nick_name
        t=OVER_FONT.render(winner,1,BLACK)
        WIN.blit(t,(350,150))
    else:
    #board
        for x in range(8):
            for y in range(8):
                if (x+y)%2==1:
                    obj=WHITE_SQUARE.copy()
                    obj.x=y*50
                    obj.y=x*50
                    pygame.draw.rect(WIN,GREY,obj)
        #piece
        for k in PIECES_DICT:
            if PIECES_DICT[k].player==PLAYER1_SYMBOL:
                if PIECES_DICT[k].isKing:
                    p=WIN.blit(RK,PIECES_DICT[k].pos)
                    PIECES_DICT[k].surface=p
                else:
                    p=WIN.blit(RM,PIECES_DICT[k].pos)
                    PIECES_DICT[k].surface=p
            elif PIECES_DICT[k].player==PLAYER2_SYMBOL:
                if PIECES_DICT[k].isKing:
                    p=WIN.blit(BK,PIECES_DICT[k].pos)
                    PIECES_DICT[k].surface=p
                else:
                    p=WIN.blit(BM,PIECES_DICT[k].pos)
                    PIECES_DICT[k].surface=p
            #piece focus outline
            if PIECES_DICT[k].isFocus:
                pygame.draw.rect(WIN,WHITE,PIECES_DICT[k].surface,2)
                #tips for movement 
                for v in range(len(PIECES_DICT[k].move_tips_pieces)):
                    p=pygame.draw.rect(WIN,YELLOW,
                    (
                        PIECES_DICT[k].move_tips_pieces[v].pos[0],
                        PIECES_DICT[k].move_tips_pieces[v].pos[1],
                        SQUARE_SIZE,SQUARE_SIZE),2)
                    PIECES_DICT[k].move_tips_pieces[v].surface=p
    return

def draw_mouse(mouse_pos):
    txt="x:{0},y={1}".format(mouse_pos[0],mouse_pos[1])
    draw_mouse_pos_text=HEALTH_FONT.render(txt,1,BLACK)
    WIN.blit(draw_mouse_pos_text,mouse_pos)
    return 

#convert ascii to piece objs in dict
def piece_dict_update(board):
    global FOCUS_PIECE_GRID_POS
    PIECES_DICT.clear()
    for r in range(NRow):
        for c in range(NColumn):
            #all valid piece positions
            if (r+c)%2==1:
                if board[r][c]!=DARK_SQUARE:
                    if board[r][c]==PLAYER1_SYMBOL:
                        piece=PIECE()
                        piece.player=PLAYER1_SYMBOL
                        piece.pos=(location(c),location(r))
                        piece.gird_pos=(r,c)
                        PIECES_DICT[r,c]=piece
                    if board[r][c]==PLAYER1_SYMBOL+PLAYER1_SYMBOL:
                        piece=PIECE()
                        piece.player=PLAYER1_SYMBOL
                        piece.pos=(location(c),location(r))
                        piece.gird_pos=(r,c)
                        piece.isKing=True
                        PIECES_DICT[r,c]=piece
                    if board[r][c]==PLAYER2_SYMBOL:
                        piece=PIECE()
                        piece.player=PLAYER2_SYMBOL
                        piece.pos=(location(c),location(r))
                        piece.gird_pos=(r,c)
                        PIECES_DICT[r,c]=piece
                    if board[r][c]==PLAYER2_SYMBOL+PLAYER2_SYMBOL:
                        piece=PIECE()
                        piece.player=PLAYER2_SYMBOL
                        piece.pos=(location(c),location(r))
                        piece.isKing=True
                        piece.gird_pos=(r,c)
                        PIECES_DICT[r,c]=piece
    FOCUS_PIECE_GRID_POS=()
    return

def init_piece(board=None):
    if board==None:
        for x in range(8):
            for y in range(8):
                if (x+y)%2==1:
                    if x<3:
                        piece=PIECE()
                        piece.pos=(location(y),location(x))
                        piece.gird_pos=(x,y)
                        PIECES_DICT[x,y]=piece
                    elif x>4:
                        piece=PIECE()
                        piece.pos=(location(y),location(x))
                        piece.gird_pos=(x,y)
                        PIECES_DICT[x,y]=piece
    else:
        piece_dict_update(board)

def piece_focused(player,k,all_possible_moves):
    global FOCUS_PIECE_GRID_POS,PIECES_DICT
    if  k==FOCUS_PIECE_GRID_POS:
        return

    if PIECES_DICT[k].player!=player:
        return

    #focused piece changed
    if FOCUS_PIECE_GRID_POS !=():
        PIECES_DICT[k].isFocus=True
        PIECES_DICT[FOCUS_PIECE_GRID_POS].move_tips_pieces.clear()
        PIECES_DICT[FOCUS_PIECE_GRID_POS].isFocus=False
    else:
        #()
        PIECES_DICT[k].isFocus=True

    FOCUS_PIECE_GRID_POS=k

    #create move tips pieces
    if all_possible_moves !=None:
        for board_move in all_possible_moves:
            if board_move[NRow][0]==list(k):
                x=board_move[NRow][1][0]
                y=board_move[NRow][1][1]
                piece=PIECE()
                piece.pos=(location(y),location(x))
                piece.gird_pos=(x,y)
                piece.move_grid_pos=board_move[NRow]
                PIECES_DICT[k].move_tips_pieces.append(piece)    

    return

def game_replay():
    pass
#EXAMPLES
TURN_INTO_KING_1=[
    ['_', '0', '_', '0', '_', '0', '_', '0'],
    ['0', '_', '0', '_', '0', '_', '0', '_'],
    ['_', '1', '_', '0', '_', '0', '_', '0'],
    ['0', '_', '22', '_', '0', '_', '0', '_'],
    ['_', '0', '_', '0', '_', '0', '_', '0'],
    ['0', '_', '0', '_', '0', '_', '0', '_'],
    ['_', '0', '_', '0', '_', '0', '_', '0'],
    ['0', '_', '0', '_', '0', '_', '0', '_']]

#TODO
class AI_HELP:
    def __init__(self):
        self.wining_rate=0
        return
def print_ai_info(ai):
    return

#init game,ai player
#return game,2player
def load_config(board=TURN_INTO_KING_1,P1="MINIMAX",P2="HUMAN"):
    global FOCUS_PIECE_GRID_POS
    AIPLAYERS={
    'MINIMAX':MiniMaxPlayer(PLAYER1_SYMBOL,10,"MINIMAX PLAYER"),
    "Q":QLaerning(PLAYER1_SYMBOL,1000,"Q-Learning PLAYER"),
    "MCTS":MCTS(PLAYER1_SYMBOL,1000,"MCTS PLAYER"),
    "HUMAN":Human(PLAYER2_SYMBOL,True,"YOU")}

    game=Draughts(PLAYER2_SYMBOL,board)
    init_piece(game.board)

    GAMEPLAYERS={
        PLAYER1_SYMBOL:AIPLAYERS[P1],
        PLAYER2_SYMBOL:AIPLAYERS[P2],
    }

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    StartGame(game,GAMEPLAYERS)
                    return

        WIN.fill(WHITE)
        tutorial_text=[
            "1. This is a board game Draughts.",
            "2. Feel free to play even without experience.",
            "3. Your opponent is AI player and try the best to defeat it.",
            "4. You should play 6 rounds to finish this test.",
            "5. Follow the tips for further details.",
            "6. Press [SPACE] to start"]
        for i in range(len(tutorial_text)):
            t=TUTOR_FONT.render(tutorial_text[i],1,BLACK)
            WIN.blit(t,(WIN.get_rect().centerx-300,50+i*50))
        pygame.display.update()



#entry
def StartGame(game,GAMEPLAYERS):
    clock = pygame.time.Clock()
    next_possbile_states=None
    while True:
        clock.tick(FPS)
        player=GAMEPLAYERS[game.current_player]
        if not game.isGameOver():
            #generated all possible movements
            if next_possbile_states == None:
                next_possbile_states=game.Movement(game.board,game.current_player)
            
            #select one movement by AI or Human
            if next_possbile_states!=None:
                board_move=player.chooseMove(game,next_possbile_states)
                if board_move!=None:
                    selected_board=board_move[0]
                    selected_move=board_move[1]
                    game.update(selected_board,selected_move)
                    piece_dict_update(game.board)
                    next_possbile_states=None
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                #human input 
                pos=pygame.mouse.get_pos()
                if player.isHuman:
                    for k in PIECES_DICT:
                        if PIECES_DICT[k].surface.collidepoint(pos):
                            print(k)
                            piece_focused(player.player_piece,k,next_possbile_states)

                        #choose action
                        for piece in PIECES_DICT[k].move_tips_pieces:
                            if piece.surface!=None and piece.surface.collidepoint(pos):
                                from_grid_pos=piece.move_grid_pos[0]
                                to_grid_pos=piece.move_grid_pos[1]
                                player.get_input(from_grid_pos,to_grid_pos)

            #test
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    StartGame(game,GAMEPLAYERS)

            print(event)

        #Drawing
        update_draw(game,player)
        draw_mouse(pygame.mouse.get_pos())                            
        pygame.display.flip()

    main()


if __name__ == "__main__":
    load_config()