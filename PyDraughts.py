from multiprocessing import connection
import pygame
import os
from GI import *
from Draughts import *


pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draughts with AI")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY=(90,90,90)

SQUARE_SIZE=50
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
PIECE_RADIUS=25


def location(x):
    return  x*SQUARE_SIZE

def piece_location(x):
    return x*PIECE_RADIUS+PIECE_RADIUS/2

KING_SIZE=4
def draw_board(board):
    # WIN.blit(SPACE, (0, 0))
    for r in range(NRow):
        for c in range(NColumn):
            if board[r][c]==DARK_SQUARE:
                rect_square=pygame.Rect(location(r),location(c),SQUARE_SIZE,SQUARE_SIZE)
                pygame.draw.rect(WIN,GREY,rect_square)
            if board[r][c]==WHITE_SQUARE:
                rect_square=pygame.Rect(location(r),location(c),SQUARE_SIZE,SQUARE_SIZE)
                pygame.draw.rect(WIN,WHITE,rect_square)
            if board[r][c]==PLAYER1:
                pygame.draw.circle(WIN,RED,(piece_location(r),piece_location(c)),PIECE_RADIUS,0)
            if board[r][c]==PLAYER2:
                pygame.draw.circle(WIN,BLACK,(piece_location(r),piece_location(c)),PIECE_RADIUS,0)
            if board[r][c]==PLAYER1+PLAYER1:
                pygame.draw.polygon(WIN,RED,
                                        [(0*KING_SIZE+piece_location(c),2*KING_SIZE+piece_location(r)),
                                         (3*KING_SIZE+piece_location(c),6*KING_SIZE+piece_location(r)),
                                         (5*KING_SIZE+piece_location(c),0*KING_SIZE+piece_location(r)),
                                         (7*KING_SIZE+piece_location(c),6*KING_SIZE+piece_location(r)),
                                         (10*KING_SIZE+piece_location(c),2*KING_SIZE+piece_location(r)),
                                         (9*KING_SIZE+piece_location(c),10*KING_SIZE+piece_location(r)),
                                         (1*KING_SIZE+piece_location(c),10*KING_SIZE+piece_location(r))])
            if board[r][c]==PLAYER2+PLAYER2:
                pygame.draw.polygon(WIN,BLACK,
                                        [(0*KING_SIZE+piece_location(c),2*KING_SIZE+piece_location(r)),
                                         (3*KING_SIZE+piece_location(c),6*KING_SIZE+piece_location(r)),
                                         (5*KING_SIZE+piece_location(c),0*KING_SIZE+piece_location(r)),
                                         (7*KING_SIZE+piece_location(c),6*KING_SIZE+piece_location(r)),
                                         (10*KING_SIZE+piece_location(c),2*KING_SIZE+piece_location(r)),
                                         (9*KING_SIZE+piece_location(c),10*KING_SIZE+piece_location(r)),
                                         (1*KING_SIZE+piece_location(c),10*KING_SIZE+piece_location(r))])
            

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    pygame.display.update()


def piece_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    clock = pygame.time.Clock()
    run = True

    #game init
    game=Draughts()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw_board(game)
        mouse_pressed=pygame.mouse.get_pressed(3)
        piece_handle_movement(mouse_pressed)


    main()


if __name__ == "__main__":
    main()