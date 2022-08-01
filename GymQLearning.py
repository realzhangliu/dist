from DraughtsGameCore import *
from AIPlayers import *
from gym import Env
from gym.spaces import Discrete,Dict
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
        self.action_space = Discrete(len(self.possible_states))
        # Temperature array
        self.board_ID=BoardToStr(self.game.board)
        self.observation_space = Dict({self.board_ID:Discrete(1)})
        # Set start temp
        self.state = self.board_ID
        return self.state
    

env = ShowerEnv()

episodes = 5
winner=[]
episode=[]
player2_reward=[]
for e in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done:
        #env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score+=reward
    print('Episode:{} Score:{} {}'.format(e, score,info))

    episode.append(e)
    winner.append(info["winner"])
    player2_reward.append(score)

print(episode)
print(winner)
print(player2_reward)




alpha = 0.1
gamma = 0.6
epsilon = 0.5
q_table = {}

num_of_episodes = 1000

def updateQtable(state,action,reward):
    if state not in q_table.keys():
        q_table[state]={}
    
    if action not in q_table[state]:
        q_table[state][action]=reward
        return

    q_table[state][action]=reward
    return
    
def getMaxQtableValue(state):
    if state not in q_table.keys():
        return 0

    valueList=list(q_table[state].values())
    maxIndex=np.argmax(valueList)
    action=list(q_table[state].keys())[maxIndex]
    
    return action

def getQtableValue(state,action):
    if state not in q_table.keys():
        return 0
    if action not in q_table[state]:
        return 0
    v=q_table[state][action]
    return v

s_time=time.time()
for episode in range(0, num_of_episodes):
    # Reset the enviroment
    state = env.reset()

    # Initialize variables
    reward = 0
    done = False
    
    
    while not done:
        # Take learned path or explore new actions based on the epsilon
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = getMaxQtableValue(state)

        # Take action    
        next_state, reward, done, info = env.step(action) 
        
        # Recalculate
        q_value = getQtableValue(state,action)
        max_value = getMaxQtableValue(state)
        new_q_value = (1 - alpha) * q_value + alpha * (reward + gamma * max_value)
        
        # Update Q-table
        # q_table[state, action] = new_q_value
        updateQtable(state,action,new_q_value)
        state = next_state
    if (episode + 1) % 100 == 0:
        print("Episode: {} duration: {:.3f}".format(episode + 1,time.time()-s_time))
        s_time=time.time()

print("**********************************")
print("Training is done!\n")
print("**********************************")


total_epochs = 0
total_penalties = 0
num_of_episodes = 100

for _ in range(num_of_episodes):
    state = env.reset()
    epochs = 0
    penalties = 0
    reward = 0
    
    done = False
    
    while not done:
        action = getMaxQtableValue(state)
        state, reward, done, info = env.step(action)

        if reward < 0:
            penalties += 1

        epochs += 1

    total_penalties += penalties
    total_epochs += epochs

print("**********************************")
print("Results")
print("**********************************")
print("Epochs per episode: {}".format(total_epochs / num_of_episodes))
print("Penalties per episode: {}".format(total_penalties / num_of_episodes))