import re
from DraughtsGameCore import *
from AIPlayers import *
from gym import Env
from gym.spaces import Discrete, Box,Dict,MultiDiscrete
import numpy as np
import random


def BoardToStr(board):
    value=""
    for x in range(8):
        for y in range(8):
            if (x+y)%2==1:
                if board[x][y]!=DARK_SQUARE:
                    value+="{0},{1},{2}-".format(x,y,board[x][y])
    return value

def StrToBoard(str):
    blankBorad=[[(WHITE_SQUARE if y%2==0 else DARK_SQUARE )if x%2==0 else (DARK_SQUARE if y%2==0 else WHITE_SQUARE) for y in range(NColumn)] for x in range(NRow)]
    #vv=["1,2,1","2,1,2",...]
    for vv in str.split('-'):
        if vv=="":
            continue
        else:
            #vvv=["1","2","1"]
            vvv=vv.split(",")
            blankBorad[int(vvv[0])][int(vvv[1])]=vvv[2]
    return blankBorad
                
            

class ShowerEnv(Env):
    def __init__(self):
        #init game
        self.game=Draughts(PLAYER2_SYMBOL)
        #all possible game state with movement
        self.possible_states=self.game.Movement(self.game.board,self.game.current_player)
        # Actions
        self.action_space = Discrete(len(self.possible_states))
        # map 2-dimension array to a string ID
        self.board_ID=BoardToStr(self.game.board)
        # 
        self.observation_space = Dict({self.board_ID:Discrete(1)})
        # Set start temp
        self.state = self.board_ID
        
    def step(self, action):
        # Apply action
        selected_board=self.possible_states[action][:NRow]
        self.game.update(selected_board)

        info={}

        if self.game.isGameOver():
            reward=self.game.evalState(selected_board)
            done=True
            info = {"winner":self.game.getWinner(self.game.board)}
            return "",reward,done,info
        else:
            done=False
        
        #opponent play action randomly
        possible_states=self.game.Movement(self.game.board,PLAYER1_SYMBOL)
        player1_action_index=random.randint(0,len(possible_states)-1)
        player1_selected_board=possible_states[player1_action_index][:NRow]
        self.game.update(player1_selected_board)
        self.state = BoardToStr(player1_selected_board)

        if self.game.isGameOver():
            reward=self.game.evalState(player1_selected_board)
            done=True
            info = {"winner":self.game.getWinner(self.game.board)}
            return "",reward,done,info
        else:
            done=False

        # Calculate reward
        reward=self.game.evalState(player1_selected_board)
        # print("reward: {0}".format(reward))

        #for player 2
        self.possible_states=self.game.Movement(self.game.board,PLAYER2_SYMBOL)
        self.action_space = Discrete(len(self.possible_states))
        # Temperature array
        self.board_ID=BoardToStr(self.game.board)
        self.observation_space = Dict({self.board_ID:Discrete(1)})

        # Return step information
        return self.state, reward, done, info

    def render(self):
        # Implement viz
        pass
    
    def reset(self):
        #init game
        self.game=Draughts(PLAYER2_SYMBOL)
        #all possible game state with movement
        self.possible_states=self.game.Movement(self.game.board,self.game.current_player)[:NRow]
        # Actions we can take, down, stay, up
        # self.action_space = Dict({"position": Discrete(2), "velocity": Discrete(3)})
        self.action_space = Discrete(len(self.possible_states))
        # Temperature array
        self.board_ID=BoardToStr(self.game.board)
        self.observation_space = Dict({self.board_ID:Discrete(1)})
        # Set start temp
        self.state = self.board_ID
        return self.state
    

env = ShowerEnv()
print(env.observation_space.sample())


episodes = 10
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done:
        #env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score+=reward
    print('Episode:{} Score:{} {}'.format(episode, score,info))
