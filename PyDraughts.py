import pygame
import os
from GameFramework import *
from DraughtsGameCore import *
from AIPlayers import *
from PyDraughtsUtil import *
import random
import string

#game utils
def location(x):
    return  x*SQUARE_SIZE

def piece_location(x):
    return x*PIECE_RADIUS+PIECE_RADIUS/2

def update_draw(game):
    global GAME_CURRENT_FUNCTION,REPLAY_INDEX
    WIN.fill(BOARD)
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
    #board coordination
    for x in range(8):
        for y in range(8):
            if (x+y)%2==1:
                #board mark
                mark_t=BOARD_MARK_FONT.render("{0},{1}".format(x,y),1,BOARD_MARK)
                WIN.blit(mark_t,(y*50,x*50))

    if GAME_CURRENT_FUNCTION==0:
    #game end drawing
        if game.isOver:
            if game.winner == 0:
                winner="DRAW"
            else:
                winner=GAMEPLAYERS[game.winner].nick_name
                winner+=" have won the game"
            t=OVER_FONT.render(winner,1,RED)
            WIN.blit(t,(WIN.get_rect().centerx,50))
            restart_txt=OVER_FONT.render("Press any KEY to continue",1,BLACK)
            WIN.blit(restart_txt,(WIN.get_rect().centerx,100))
        else:
        #tips
            y_axis=2
            if REVERSE_ROUND+1 in ENABLE_AI_HELP:
                lables=GAMEPLAYERS["1"].get_ai_help()
                for i in range(len(lables)):
                    if i%2!=1:
                        t=TIP_FONT.render(lables[i],1,BLACK)
                        WIN.blit(t,(WIN.get_rect().centerx+10,y_axis))
                        y_axis+=15
                    else:
                        t=BOARD_MARK_FONT.render(lables[i],1,GREY)
                        WIN.blit(t,(WIN.get_rect().centerx+10,y_axis))
                        y_axis+=30
            else:
                title=TIP_FONT.render("AI HELP DISABLE",1,BLACK)
                WIN.blit(title,(WIN.get_rect().centerx+10,y_axis))
                y_axis+=20
            round_t=TIP_FONT.render("ROUNDS: {0}".format(REVERSE_ROUND+1),1,BLACK)
            WIN.blit(round_t,(WIN.get_rect().centerx+10,y_axis))

    if GAME_CURRENT_FUNCTION==1:
        replay_text=[
            "GAME REPLAY MODE",
            "Review the movements",
            "LEFT MOUSE BUTTON to move forward",
            "RIGHT MOUSE BUTTON to move back",
            "CURRENT STEP: {0}".format(REPLAY_INDEX)]
        for i in range(len(replay_text)):
            t=TIP_FONT.render(replay_text[i],1,BLACK)
            WIN.blit(t,(WIN.get_rect().centerx,50+i*50))
            
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
#return game,2player22
def load_config(board=None,P1="MINIMAX",P2="HUMAN"):

    global FOCUS_PIECE_GRID_POS,PLAYERLISTS,GAMEPLAYERS,ROUND,REVERSE_ROUND,GAME_CURRENT_FUNCTION

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    return
            if ROUND>0:
                if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
                    PLAYERLISTS={
                    'MINIMAX':MiniMaxPlayer(PLAYER1_SYMBOL,1,"MINIMAX AI"),
                    "Q":QLaerning(PLAYER1_SYMBOL,1000,"Q-Learning AI"),
                    "HUMAN":Human(PLAYER2_SYMBOL,True,"YOU")
                    }
                    GAMEPLAYERS={
                        PLAYER1_SYMBOL:PLAYERLISTS[P1],
                        PLAYER2_SYMBOL:PLAYERLISTS[P2],
                    }
                    game=Draughts(PLAYER2_SYMBOL,board)
                    init_piece(game.board)
                    StartGame(game,GAMEPLAYERS,REPLAY_UTIL)
                    #game replay
                    if REVERSE_ROUND+1 in ENABLE_AI_HELP:
                        GAME_CURRENT_FUNCTION=1
                        StartReplay(REVERSE_ROUND)
                        GAME_CURRENT_FUNCTION=0
                    #move on next round
                    ROUND-=1
                    REVERSE_ROUND+=1
            else:
                # dump replay data
                letters = string.ascii_lowercase
                id=''.join(random.choice(letters) for i in range(10))
                REPLAY_UTIL.save_to_file(os.path.join("./Data","{0}.json".format(id)))
                pygame.quit()
                return

        WIN.fill(WHITE)
        tutorial_text=[
            "1. This is a board game Draughts.",
            "2. Feel free to play even without experience.",
            "3. You should play {0} round(s) to finish this test.".format(ROUND),
            "4. AI tips prompts and game replays will help you get learned",
            "5. Press any KEY to start or ESC to quit."]
        for i in range(len(tutorial_text)):
            t=TUTOR_FONT.render(tutorial_text[i],1,BLACK)
            WIN.blit(t,(WIN.get_rect().centerx-350,50+i*50))
        pygame.display.update()


#entry
def StartGame(game,GAMEPLAYERS,replay_util):
    global ROUND,REVERSE_ROUND
    clock = pygame.time.Clock()
    next_possbile_states=None

    player=GAMEPLAYERS[game.current_player]
    replay_util.append_step(REVERSE_ROUND,game.board,[],player.win_rate,player.initial_depth,player.algorithm)

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
                    game.update(selected_board)
                    piece_dict_update(game.board)
                    next_possbile_states=None
                    #replay add every step
                    replay_util.append_step(REVERSE_ROUND,selected_board,selected_move,player.win_rate,player.initial_depth,player.algorithm)

        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
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
                #replay add this game
                replay_util.append_game(REVERSE_ROUND)
                return
            print(event)

        #Drawing
        update_draw(game)
        # draw_mouse(pygame.mouse.get_pos())                            
        pygame.display.flip()

def StartReplay(round):
    global REPLAY_INDEX
    run=True
    game=Draughts(PLAYER2_SYMBOL)
    games,len_steps=REPLAY_UTIL.get_this_round_games(round)
    REPLAY_INDEX=0
    piece_dict_update(games[REPLAY_INDEX])
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if REPLAY_INDEX==len_steps-1:
                        return

                    if REPLAY_INDEX<len_steps-1:
                        REPLAY_INDEX+=1
                    piece_dict_update(games[REPLAY_INDEX])


                if event.button==3:
                    if REPLAY_INDEX>0:
                        REPLAY_INDEX-=1
                    piece_dict_update(games[REPLAY_INDEX])

        update_draw(game)
        pygame.display.update()
    pass
if __name__ == "__main__":
    load_config()