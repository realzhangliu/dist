from time import clock_getres
from webbrowser import get
import pygame
from Draughts import WHITE_SQUARE

from PyDraughts import BLACK, GREY


pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("test windows")
WIN=pygame.display.set_mode((400,400))

TEXT_FONT = pygame.font.SysFont('comicsans', 40)

WHITE_SQUARE=pygame.Rect(0,0,50,50)

def board():
    for x in range(8):
        for y in range(8):
            if (x+y)%2==1:
                obj=WHITE_SQUARE.copy()
                obj.x=x*50
                obj.y=y*50
                pygame.draw.rect(WIN,GREY,obj)
                

def draw_window():
    WIN.fill((255,255,255))
    board()
    text="BBB"
    mouse_pos=pygame.mouse.get_pos()
    text=str(mouse_pos[0])+","+str(+mouse_pos[1])
    mouse_pos_text=TEXT_FONT.render(text,1,BLACK)
    WIN.blit(mouse_pos_text,(mouse_pos[0],mouse_pos[1]))
    pygame.display.update()

def main():

    clock=pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                return
        draw_window()

    return



if __name__=="__main__":
    main()