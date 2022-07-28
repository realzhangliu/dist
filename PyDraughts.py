from glob import glob
from multiprocessing import connection
from re import T
from shutil import move
from tkinter.messagebox import NO
from turtle import pos
import pygame
import os
from GameFramework import *
from Draughts import *
from AIPlayers import *
from PyDraughtsConfig import *

#game utils
def location(x):
    return  x*SQUARE_SIZE

def piece_location(x):
    return x*PIECE_RADIUS+PIECE_RADIUS/2

def update_draw(game):
    WIN.fill(BOARD)
    if game.isOver:
        if game.winner == 0:
            winner="DRAW"
        else:
            winner=GAMEPLAYERS[game.winner].nick_name
            winner+=" have won the game"
        t=OVER_FONT.render(winner,1,RED)
        WIN.blit(t,(170,130))
        restart_txt=OVER_FONT.render("Press any KEY to continue",1,BLACK)
        WIN.blit(restart_txt,(170,170))
    else:
    #board
        for x in range(8):
            for y in range(8):
                if (x+y)%2==1:
                    obj=WHITE_SQUARE_RECT.copy()
                    obj.x=y*50
                    obj.y=x*50
                    pygame.draw.rect(WIN,GREY,obj)
                    #board mark
                    mark_t=BOARD_MARK_FONT.render("{0},{1}".format(x,y),1,BOARD_MARK)
                    WIN.blit(mark_t,(y*50,x*50))
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

        for x in range(8):
            for y in range(8):
                if (x+y)%2==1:
                    #board mark
                    mark_t=BOARD_MARK_FONT.render("{0},{1}".format(x,y),1,BOARD_MARK)
                    WIN.blit(mark_t,(y*50,x*50))
        #tips
        lables=GAMEPLAYERS["1"].get_ai_help()
        y_axis=2
        for i in range(len(lables)):
            if i%2!=1:
                t=TIP_FONT.render(lables[i],1,BLACK)
                WIN.blit(t,(WIN.get_rect().centerx+10,y_axis))
                y_axis+=15
            else:
                t=BOARD_MARK_FONT.render(lables[i],1,GREY)
                WIN.blit(t,(WIN.get_rect().centerx+10,y_axis))
                y_axis+=30
        round_t=TIP_FONT.render("ROUNDS: {0}".format(ROUND),1,BLACK)
        WIN.blit(round_t,(WIN.get_rect().centerx+10,y_axis))
            
            
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
TEST_GAME_STATE=[
    ['_', '0', '_', '0', '_', '0', '_', '0'],
    ['0', '_', '0', '_', '0', '_', '0', '_'],
    ['_', '1', '_', '0', '_', '0', '_', '0'],
    ['0', '_', '2', '_', '0', '_', '0', '_'],
    ['_', '0', '_', '0', '_', '0', '_', '0'],
    ['0', '_', '0', '_', '0', '_', '0', '_'],
    ['_', '0', '_', '0', '_', '0', '_', '0'],
    ['0', '_', '0', '_', '0', '_', '0', '_']]


#init game,ai player
#return game,2player
def load_config(board=None,P1="MINIMAX",P2="HUMAN"):

    global FOCUS_PIECE_GRID_POS,PLAYERLISTS,GAMEPLAYERS,ROUND

    PLAYERLISTS={
    'MINIMAX':MiniMaxPlayer(PLAYER1_SYMBOL,4,"MINIMAX AI"),
    "Q":QLaerning(PLAYER1_SYMBOL,1000,"Q-Learning AI"),
    "MCTS":MCTS(PLAYER1_SYMBOL,1000,"MCTS AI"),
    "HUMAN":Human(PLAYER2_SYMBOL,True,"YOU")}

    GAMEPLAYERS={
        PLAYER1_SYMBOL:PLAYERLISTS[P1],
        PLAYER2_SYMBOL:PLAYERLISTS[P2],
    }

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
                if ROUND>0:
                    game=Draughts(PLAYER2_SYMBOL,board)
                    init_piece(game.board)
                    StartGame(game,GAMEPLAYERS)
                else:
                    pygame.quit()
                    return

        WIN.fill(WHITE)
        tutorial_text=[
            "1. This is a board game Draughts.",
            "2. Feel free to play even without experience.",
            "3. Your opponent is an AI player and try the best to defeat it.",
            "4. You should play {0} round(s) to finish this test.".format(ROUND),
            "5. Follow the tips for further details.",
            "6. Press any KEY to start"]
        for i in range(len(tutorial_text)):
            t=TUTOR_FONT.render(tutorial_text[i],1,BLACK)
            WIN.blit(t,(WIN.get_rect().centerx-350,50+i*50))
        pygame.display.update()



#entry
def StartGame(game,GAMEPLAYERS):
    global ROUND
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


            if (event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN) and game.isOver:
                ROUND-=1
                return
            print(event)

        #Drawing
        update_draw(game)
        draw_mouse(pygame.mouse.get_pos())                            
        pygame.display.flip()

    main()


if __name__ == "__main__":
    load_config()