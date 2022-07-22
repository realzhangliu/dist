from multiprocessing import connection
from turtle import pos
import pygame
import os
from GI import *
from Draughts import *
from AIPlayers import *


#pygame init
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 800, 400
pygame.display.set_caption("Draughts with AI")
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

#game init
WHITE = (240, 240, 240)
BOARD=(180,180,180)
BLACK = (39, 39, 39)
RED = (154, 34, 20)
YELLOW = (255, 255, 0)
GREY=(90,90,90)
SQUARE_SIZE=50
PIECE_RADIUS=50

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
    pos=()
    color=None
    surface=None
    isKing=False
    isFocus=False
    gird_pos=()
    move_tips_pieces=[]

FOCUS_PIECE_GRID_POS=()

def init_piece():
    for x in range(8):
        for y in range(8):
            if (x+y)%2==1:
                if x<3:
                    piece=PIECE()
                    piece.color=RED
                    piece.pos=(location(y),location(x))
                    piece.radius=PIECE_RADIUS/2
                    piece.gird_pos=(x,y)
                    PIECES_DICT[x,y]=piece
                elif x>4:
                    piece=PIECE()
                    piece.color=BLACK
                    piece.pos=(location(y),location(x))
                    piece.radius=PIECE_RADIUS/2
                    piece.gird_pos=(x,y)
                    PIECES_DICT[x,y]=piece

def update_draw():
    WIN.fill(BOARD)
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
        if PIECES_DICT[k].color==RED:
            if PIECES_DICT[k].isKing:
                p=WIN.blit(RK,PIECES_DICT[k].pos)
                PIECES_DICT[k].surface=p
            else:
                p=WIN.blit(RM,PIECES_DICT[k].pos)
                PIECES_DICT[k].surface=p
        elif PIECES_DICT[k].color==BLACK:
            if PIECES_DICT[k].isKing:
                p=WIN.blit(BK,PIECES_DICT[k].pos)
                PIECES_DICT[k].surface=p
            else:
                p=WIN.blit(BM,PIECES_DICT[k].pos)
                PIECES_DICT[k].surface=p
        #piece focus outline
        if PIECES_DICT[k].isFocus:
            pygame.draw.rect(WIN,WHITE,PIECES_DICT[k].surface,2)
        #TODO
        #piece movement tips

    return


def draw_mouse(mouse_pos):
    txt="x:{0},y={1}".format(mouse_pos[0],mouse_pos[1])
    draw_mouse_pos_text=HEALTH_FONT.render(txt,1,BLACK)
    WIN.blit(draw_mouse_pos_text,mouse_pos)
    return 

def piece_update(board,pos):
    #TODO
    #add,del,piece
    #del thisdict["model"]
    return


def main():
    global FOCUS_PIECE_GRID_POS

    game=Draughts(PLAYER1_SYMBOL)

    AIPLAYERS={
        'MINIMAX':MiniMaxPlayer(PLAYER1_SYMBOL,4),
        "Q":QLaerning(PLAYER1_SYMBOL,1000),
        "MCTS":MCTS(PLAYER1_SYMBOL,1000),
        "HUMAN":Human(PLAYER2_SYMBOL,True)}

    GAMEPLAYERS={
        PLAYER1_SYMBOL:AIPLAYERS["MINIMAX"],
        PLAYER2_SYMBOL:AIPLAYERS["HUMAN"]
    }

    init_piece()

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        #EVENTS
        if game.isGameOver():
            continue
        else:
            player=GAMEPLAYERS[game.current_player]
            next_possbile_states=game.Movement(game.board,game.current_player)
            board_pos=player.chooseMove(next_possbile_states)
            if board_pos==None:
                continue
            else:
                game.update(board_pos[0],board_pos[1])
            
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
                            if FOCUS_PIECE_GRID_POS!=k and FOCUS_PIECE_GRID_POS !=():
                                PIECES_DICT[k].isFocus=True
                                PIECES_DICT[k].move_grid_pos=[]
                                PIECES_DICT[FOCUS_PIECE_GRID_POS].move_grid_pos=[]
                                PIECES_DICT[k].move_tips_rect=[]
                                PIECES_DICT[FOCUS_PIECE_GRID_POS].move_tips_rect=[]
                                PIECES_DICT[FOCUS_PIECE_GRID_POS].isFocus=False
                                FOCUS_PIECE_GRID_POS=k
                            else:
                                FOCUS_PIECE_GRID_POS=k
                                PIECES_DICT[FOCUS_PIECE_GRID_POS].isFocus=True
                        #choose action
                        for move_tips_piece in PIECES_DICT[k].move_tips_pieces:
                            if move_tips_piece.surface.collidepoint(pos):
                                from_grid_pos=PIECES_DICT[k].grid_pos
                                to_grid_pos=move_tips_piece.grid_pos
                                player.get_input(from_grid_pos,to_grid_pos)

            #test
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    PIECES_DICT[2,1].pos=(300,77)

            print(event)

        piece_update(game.board)
        #Drawing
        update_draw()
        draw_mouse(pygame.mouse.get_pos())                            
        pygame.display.flip()

    main()


if __name__ == "__main__":
    main()