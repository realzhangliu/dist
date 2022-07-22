from GI import Player
from Draughts import *
import math

class MiniMaxPlayer(Player):
    def __init__(self, piece, initial_depth):
        super().__init__(piece)
        self.initial_depth = max(1, initial_depth)
        self.g=None
    
    def chooseMove(self, game):
        self.g=game
        # bestValue, bestMove = self.alphabeta(game, self.initial_depth, -self.INFINITY, self.INFINITY)
        newState,newPos=self.MinimaxDecision(self.g.board)
        return newState,newPos

    def chooseMove(self, game,possible_states):
        self.g=game
        # bestValue, bestMove = self.alphabeta(game, self.initial_depth, -self.INFINITY, self.INFINITY)
        newState,newPos=self.MinimaxDecision(possible_states)
        return newState,newPos

    #alpha beta algorithm implementation
    def MinimaxDecision(self,possible_states):
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
        return newState,newPos

    def MinValue(self,curState,alpha,beta,depth):
        #test won 
        if self.g.checkWhoWon(curState)==self.player_piece:
            return 20
        if self.g.checkWhoWon(curState)!=self.player_piece:
            return -20
        # draw ?, AI never give up
        #test eval
        if depth==0:
            return self.g.evalState(curState)
        minValue=24
        for v in self.g.Movement(curState,PLAYER2_SYMBOL):
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
        #test won 
        if self.g.checkWhoWon(curState)==self.player_piece:
            return 20
        if self.g.checkWhoWon(curState)!=self.player_piece:
            return -20
        # draw ?, AI never give up
        #test eval
        if depth==0:
            return self.g.evalState(curState)
        maxValue=-20
        for v in self.g.Movement(curState,PLAYER1_SYMBOL):
            v=v[:NRow]
            val=self.MinValue(v,alpha,beta,depth-1)
            if val>maxValue:
                maxValue=val
            if val>beta:
                return val
            if val>alpha:
                alpha=val
        return maxValue



class QLaerning(Player):
    def __init__(self, piece, max_epoch):
        super().__init__(piece)
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
    def __init__(self, piece, max_epoch):
        super().__init__(piece)
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
    def __init__(self, piece,isHuman):
        super().__init__(piece,isHuman)
        self.g=None
    
    def chooseMove(self, game,possible_states):
        self.g=game
        if self.from_pos_input==() or self.to_pose_input==():
            return None
        else:
            for v in possible_states:
                pos=v[NRow]
                state=v[:NRow]
                for p in pos:
                    if p[0]==list(self.from_pos_input) and p[1]==list(self.to_pose_input[1]):
                        self.from_pos_input=()
                        self.to_pose_input=()
                        return state,pos
        return None