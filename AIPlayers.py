from turtle import pos
from GameFramework import Player
from Draughts import *
import math
from PyDraughtsConfig import *
import time

class MiniMaxPlayer(Player):
    def __init__(self, piece, initial_depth,nick_name):
        super().__init__(piece,False,nick_name)
        self.initial_depth = max(1, initial_depth)
        self.g=None
        self.aiinfo=AIHELP(self)
        self.value=-24
        self.move=[]
        self.tc=0
        self.update_ai_info()

    def chooseMove(self, game,possible_states):
        self.g=game
        if self.g.current_player!=self.player_piece:
            raise ValueError('Wrong current player round.')
        # bestValue, bestMove = self.alphabeta(game, self.initial_depth, -self.INFINITY, self.INFINITY)
        newState,newPos,value,time_count=self.MinimaxDecision(possible_states)
        self.value=value
        self.move=newPos
        self.tc=time_count
        self.update_ai_info()
        return newState,newPos

    #alpha beta algorithm implementation
    def MinimaxDecision(self,possible_states):
        s_time=time.time()
        maxValue=-24
        newState=None
        newPos=[]
        #vv list contains multiple different game baords after AI agent taking various actions, then evaluate.
        for v in possible_states:
            #splite the board and postion detail that Ai agent took.
            pos=v[NRow]
            #game board state
            v=v[:NRow]
            val=self.MinValue(v,-math.inf,math.inf,self.initial_depth)
            if val>maxValue:
                maxValue=val
                newState=v
                newPos=pos[:]
        return newState,newPos,val,time.time()-s_time

    def MinValue(self,curState,alpha,beta,depth):
        #test won 
        winner=self.g.getWinner(curState)
        if winner==self.player_piece:
            return 20
        if winner!=-1 and winner!=self.player_piece:
            return -20
        # if self.g.checkWhoWon(curState)==self.player_piece:
        #     return 20
        # if self.g.checkWhoWon(curState)!=self.player_piece:
        #     return -20
        # draw ?, AI never give up
        #test eval
        if depth==0:
            return self.g.evalState(curState)
        minValue=24
        
        # opponent= PLAYER2_SYMBOL if self.player_piece==PLAYER1_SYMBOL else PLAYER1_SYMBOL
        opponent=PLAYER2_SYMBOL if self.g.current_player==PLAYER1_SYMBOL else PLAYER2_SYMBOL
        for v in self.g.Movement(curState, opponent):
            v=v[:NRow]
            val=self.MaxValue(v,alpha,beta,depth-1)
            if val<minValue:
                minValue=val
            if val<alpha:
                return val
            if val<beta:
                beta=val
        return minValue


    def MaxValue(self,curState,alpha,beta,depth):
        winner=self.g.getWinner(curState)
        if winner==self.player_piece:
            return 20
        if winner!=-1 and winner!=self.player_piece:
            return -20
        #test won 
        # if self.g.checkWhoWon(curState)==self.player_piece:
        #     return 20
        # if self.g.checkWhoWon(curState)!=self.player_piece:
        #     return -20
        # draw ?, AI never give up
        #test eval
        if depth==0:
            return self.g.evalState(curState)
        maxValue=-20
        # ally= PLAYER1_SYMBOL if self.player_piece==PLAYER1_SYMBOL else PLAYER2_SYMBOL
        me=PLAYER1_SYMBOL if self.g.current_player==PLAYER1_SYMBOL else PLAYER2_SYMBOL
        for v in self.g.Movement(curState,me):
            v=v[:NRow]
            val=self.MinValue(v,alpha,beta,depth-1)
            if val>maxValue:
                maxValue=val
            if val>beta:
                return val
            if val>alpha:
                alpha=val
        return maxValue


    def update_ai_info(self):
        self.aiinfo.ai_algorithm="ALGORITHM: MiniMax"
        self.aiinfo.ai_algorithm_config="DEPTH: {0}".format(self.initial_depth)
        if self.initial_depth<=4:
            self.aiinfo.ai_level="DIFFICULTY: ESAY"
        if self.initial_depth>4 and self.initial_depth<=7:
            self.aiinfo.ai_level="DIFFICULTY: MEDIUM"
        if self.initial_depth>7:
            self.aiinfo.ai_level="DIFFICULTY: HARD"
        self.aiinfo.ai_name="AI PLAYER: {0}".format(self.nick_name)
        self.aiinfo.current_confidence="CONFIDENCE: {0}".format(self.value+24)
        self.aiinfo.current_movement="MOVEMENT: {0}".format(self.move)
        self.aiinfo.estimated_win_rate="WIN RATE: ~{0:.3f}%".format((self.value+24)/120*100)
        self.aiinfo.process_time="DURATION: {0:.2f}s".format(round(self.tc))
        return
    def get_ai_help(self):
        return self.aiinfo.get_info_text()


class QLaerning(Player):
    def __init__(self, piece, max_epoch,nick_name):
        super().__init__(piece,False,nick_name)
        self.max_epoch = max(1, max_epoch)
        self.g=None
    
    def chooseMove(self, game,possible_states):
        self.g=game
        # bestValue, bestMove = self.alphabeta(game, self.initial_depth, -self.INFINITY, self.INFINITY)
        newState,newPos=self.BestAction(self.g.board)
        return newState,newPos

    #alpha beta algorithm implementation
    def BestAction(self,curState):
        maxValue=-24
        newState=None
        newPos=[]
        #vv list contains multiple different game baords after AI agent taking various actions, then evaluate.
        vv=self.g.Movement(curState,self.player_piece)
        for v in vv:
            #splite the board and postion detail that Ai agent took.
            pos=v[NRow]
            #game board state
            v=v[:NRow]
            val=self.MinValue(v,-math.inf,math.inf,self.initial_depth)
            if val>maxValue:
                maxValue=val
                newState=v
                newPos=pos[:]
        return newState,newPos


class MCTS(Player):
    def __init__(self, piece, max_epoch,nick_name):
        super().__init__(piece,False,nick_name)
        self.max_epoch = max(1, max_epoch)
        self.g=None
    
    def chooseMove(self, game,possible_states):
        self.g=game
        # bestValue, bestMove = self.alphabeta(game, self.initial_depth, -self.INFINITY, self.INFINITY)
        newState,newPos=self.BestAction(self.g.board)
        return newState,newPos

    #alpha beta algorithm implementation
    def BestAction(self,curState):
        maxValue=-24
        newState=None
        newPos=[]
        #vv list contains multiple different game baords after AI agent taking various actions, then evaluate.
        vv=self.g.Movement(curState,self.player_piece)
        for v in vv:
            #splite the board and postion detail that Ai agent took.
            pos=v[NRow]
            #game board state
            v=v[:NRow]
            val=self.MinValue(v,-math.inf,math.inf,self.initial_depth)
            if val>maxValue:
                maxValue=val
                newState=v
                newPos=pos[:]
        return newState,newPos

class Human(Player):
    def __init__(self, piece,isHuman,nick_name):
        super().__init__(piece,isHuman,nick_name)
        self.g=None
    def chooseMove(self, game,possible_states):
        self.g=game
        if self.from_pos_input==() or self.to_pose_input==():
            return None
        else:
            for v in possible_states:
                pos=v[NRow]
                state=v[:NRow]
                if pos[0]==self.from_pos_input and pos[1]==self.to_pose_input:
                    self.from_pos_input=()
                    self.to_pose_input=()
                    return state,pos
        return None