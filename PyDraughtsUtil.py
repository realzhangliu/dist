import re
import pygame
import os

WIDTH, HEIGHT = 800, 400

pygame.init()
pygame.font.init()
pygame.display.set_caption("Draughts with AI")
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

ROUND=3
REVERSE_ROUND=0
#0=normal 1=game replay
GAME_CURRENT_FUNCTION=0
# specify the index of round that enable AI HELP
ENABLE_AI_HELP=[2]

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



class AIHELP:
    def __init__(self,player) -> None:
        self.ai_name=""
        self.ai_name_desc="(player name)"
        self.ai_algorithm=""
        self.ai_algorithm_desc="(algorithm AI used)"
        self.ai_algorithm_config=""
        self.ai_algorithm_config_desc="(algorithm configuration)"
        self.process_time=""
        self.process_time_desc="(the time every step takes)"
        self.ai_level=""
        self.ai_level_desc="(easy|medium|hard),AI will change difficulty according to player level"
        self.estimated_win_rate=""
        self.estimated_win_rate_desc="(percentage of win rate of AI)"
        self.current_confidence=""
        self.current_confidence_desc="(score AI estimated for current decision)"
        self.current_movement=""
        self.current_movement_desc="(movement locations)"
    def get_info(self):
        info=[
            TIP_FONT.render(self.ai_name,1,BLACK),
            BOARD_MARK_FONT.render(self.ai_name_desc,1,BLACK),
            
            TIP_FONT.render(self.ai_algorithm,1,BLACK),
            BOARD_MARK_FONT.render(self.ai_algorithm_desc,1,BLACK),

            TIP_FONT.render(self.ai_algorithm_config,1,BLACK),
            BOARD_MARK_FONT.render(self.ai_algorithm_config_desc,1,BLACK),

            TIP_FONT.render(self.process_time,1,BLACK),
            BOARD_MARK_FONT.render(self.process_time_desc,1,BLACK),

            TIP_FONT.render(self.ai_level,1,BLACK),
            BOARD_MARK_FONT.render(self.ai_level_desc,1,BLACK),    

            TIP_FONT.render(self.estimated_win_rate,1,BLACK),
            BOARD_MARK_FONT.render(self.estimated_win_rate_desc,1,BLACK),

            TIP_FONT.render(self.current_confidence,1,BLACK),
            BOARD_MARK_FONT.render(self.current_confidence_desc,1,BLACK),

            TIP_FONT.render(self.current_movement,1,BLACK),
            BOARD_MARK_FONT.render(self.current_movement_desc,1,BLACK),

            TIP_FONT.render(self.current_round,1,BLACK),
            BOARD_MARK_FONT.render(self.current_round_desc,1,BLACK),
        ]
        return info
    

    def get_info_text(self):
        return [
        self.ai_name,
        self.ai_name_desc,
        self.ai_algorithm,
        self.ai_algorithm_desc,
        self.ai_algorithm_config,
        self.ai_algorithm_config_desc,
        self.process_time,
        self.process_time_desc,
        self.ai_level,
        self.ai_level_desc,
        self.estimated_win_rate,
        self.estimated_win_rate_desc,
        self.current_confidence,
        self.current_confidence_desc,
        self.current_movement,
        self.current_movement_desc,
        ]

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
    def append_step(self,round,board,move,winning_rate=0,difficulty="None",algorithm="None"):
        if len(self.round)<round+1:
            self.new_round(round)
        step={
                "board":board,
                "move":move,
                "ai_winning_rate":winning_rate,
                "difficulty":difficulty,
                "algorithm":algorithm,
                }
        self.round[round]["data"]["steps"].append(step)
        return

    #collect every game
    def append_game(self,round):
        if len(self.round)<round:
            self.new_round(round)

        self.round[round]["round"]=round
        total_steps=len(self.round[round]["data"]["steps"])
        self.round[round]["data"]["total_steps"]=total_steps
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
