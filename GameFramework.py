from abc import ABC, abstractmethod

class Game():
    
    @abstractmethod
    def __init__(self):
        self.current_player = None
    
    @abstractmethod
    def update(self, move):
        pass
    
    @abstractmethod
    def getMoves(self):
        return []
    
    @abstractmethod
    def isGameOver(self):
        return True
    
    @abstractmethod
    def getWinner(self):
        return None
    
    @abstractmethod
    def clone(self):
        pass
    
    @abstractmethod
    def drawGame(self):
        pass
    
    def evaluate(self, player_piece):
        winner = self.getWinner()
        if winner==player_piece:
            return 1
        elif winner!=None:
            return -1
        return 0
    
class Player():
    def __init__(self, piece,isHuman=False,nick_name="None"):
        self.isHuman=isHuman
        self.player_piece = piece
        self.from_pos_input=()
        self.to_pose_input=()
        self.nick_name=nick_name
    
    @abstractmethod
    def chooseMove(self, game,possible_states):
        pass

    # default evaluation method is to use the 
    # game-specific state evaluation that is
    # implemented in the game.
    def evaluate(self, state):
        return state.evaluate(self.player_piece)

    def get_input(self,from_pos,to_pos):
        self.from_pos_input=from_pos
        self.to_pose_input=to_pos