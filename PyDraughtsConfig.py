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
ROUND=6

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

#game replay
class ReplayClass:
    def __init__(self) -> None:
        pass