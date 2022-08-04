import pygame
import os

##
#configuration for pygame render
#game essential util tools
##

WIDTH, HEIGHT = 800, 400

pygame.init()
pygame.font.init()
pygame.display.set_caption("Draughts with AI Coach")
FPS = 60

HEALTH_FONT = pygame.font.SysFont('comicsans', 12)
TUTOR_FONT = pygame.font.SysFont('comicsans', 24)
OVER_FONT = pygame.font.SysFont('comicsans', 24)
TIP_FONT = pygame.font.SysFont('arial', 15)
BOARD_MARK_FONT = pygame.font.SysFont('comicsans',12)

#game init
WHITE = (240, 240, 240)
BOARD=(230,230,230)
BOARD_MARK=(180,180,180)
BLACK = (39, 39, 39)
PLAYER2_COLOR=(39, 39, 39)
RED = (154, 34, 20)
PLAYER1_COLOR=(154, 34, 20)
YELLOW = (255, 255, 0)
GREY=(90,90,90)
SQUARE_SIZE=50
PIECE_RADIUS=50

#total game round
ROUND=6
REVERSE_ROUND=0

#0= normal 1= game replay
GAME_CURRENT_FUNCTION=0

# which round has AI help 
ENABLE_AI_HELP=[3,4]

#game repaly index
REPLAY_INDEX=0

WHITE_SQUARE_RECT=pygame.Rect(0,0,50,50)


BKImg = pygame.image.load(os.path.join("Assets","BK.png"))
BK=pygame.transform.scale(BKImg,(SQUARE_SIZE,SQUARE_SIZE))

RKImg = pygame.image.load(os.path.join("Assets","RK.png"))
RK=pygame.transform.scale(RKImg,(SQUARE_SIZE,SQUARE_SIZE))

BMImg = pygame.image.load(os.path.join("Assets","BM.png"))
BM=pygame.transform.scale(BMImg,(SQUARE_SIZE,SQUARE_SIZE))

RMImg = pygame.image.load(os.path.join("Assets","RM.png"))
RM=pygame.transform.scale(RMImg,(SQUARE_SIZE,SQUARE_SIZE))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

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

PIECES_DICT={}


FOCUS_PIECE_GRID_POS=()

GAMEPLAYERS=None
PLAYERLISTS=None


import json
#game replay
#store game & load game
class ReplayUtil:
    def __init__(self) -> None:
        #for each game round
        self.step={
                    "board":[],
                    "move":[],
                    "ai_winning_rate":0,
                    "difficulty":"",
                    "algorithm":"None",
                    "player":0
                    }
        self.game={
                    "steps":[
                    ],
            "total_steps":0,
                }
        #all rounds with same player
        self.round=[
            {
            "round":0,
            "data":self.game
            }
        ]

    def get_this_round_games(self,current_round):
        board=[]
        for v in self.round[current_round]["data"]["steps"]:
            board.append(v["board"])
        return board,len(board)

    #collect every movement
    def append_step(self,round,board,move,winning_rate=0,difficulty=1,algorithm="None",player_picec=-1):
        if len(self.round)<round+1:
            self.new_round(round)
        step={
                "board":board,
                "move":move,
                "ai_winning_rate":winning_rate,
                "difficulty":difficulty,
                "algorithm":algorithm,
                "player":player_picec
                }
        self.round[round]["data"]["steps"].append(step)
        return

    #collect every game
    def append_game(self,round,winner):
        if len(self.round)<round:
            self.new_round(round)

        self.round[round]["round"]=round
        total_steps=len(self.round[round]["data"]["steps"])
        self.round[round]["data"]["total_steps"]=total_steps
        self.round[round]["data"]["winner"]=winner
        return

    #collect every round
    def new_round(self,round):
        self.round.append(
            {
                "round":round,
                "data":{
                    "steps":[
                    ],
            "total_steps":0,
            "winner":""
                }
            })
        return
        
    def load_from_file(self,file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
        self.round=data
        return self.round

    def save_to_file(self,file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open("{0}".format(file_name), 'w',encoding='utf-8') as f:
            json.dump(self.round, f,sort_keys=True, indent=4)
        return



REPLAY_UTIL=ReplayUtil()
