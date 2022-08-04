## Project:

# This project is relied on my MSc dissertation titled "Develop a artificial intelligence coach for a board game"

The aim of this project is to create an AI that plays a game not to win but to give the human player a rewarding challenge, playing in the manner of a good teacher or parent. 

![image](https://github.com/realzhangliu/dist/blob/master/screenshot.png)

## Content 

`PyDrauhts.py` is game entry for conduncting the test and collect the data for analysis.

`PyDraughtsUtil.py` includes some essential tools and configuration for initialization.

`DraughtsGameCore.py` is the implementation of the draughts, providing necessary interfaces that can interchanging data with Pygame package.

`AIPlayers.py` act as AI player class for this game.

`GameFramework.py` defines parent classes, such as Game, Player class.

`GymQLearning.ipynb` wraps the game using Gym library for training Q-Learning model. It also contains data analysis from algorithms comparison.

`GameDataAnalysis.ipynb` analysis of data from `PyDraughts.py`

## How to run as order by dissertation

1. get and analysis the result from algorithms' competition by running `GymQLearning.ipynb`

2. collect the data from human participants by running `PyDraughts.py`

3. analysis the data using by `GameDataAnalysis.ipynb`