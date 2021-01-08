import pygame
from random import randint

# graphic sizes:
# lad.png : 64px * 64px
# snk.png : 64px * 64px
# ico.png : 32px * 32px
# bg.jpeg : 1080px * 720px


# initial player coords
(x,y) = (540,576)

# player and enemy icons
icon_player = pygame.image.load('lad.png')
icon_enemy = pygame.image.load('snk.png')

# initialize pygame
pygame.init()

# display, title and icon
screen = pygame.display.set_mode((1080,720))
pygame.display.set_icon(pygame.image.load('ico.png'))
pygame.display.set_caption('Snakes vs. Space')

# ladder
def ladder(x,y):
    screen.blit(icon_player,(x,y))

# snake
def snake(x,y):
    screen.blit(icon_enemy, (x,y))

# game loop
def game():
    global x,y
    Xchange = Ychange = 0 # 
    
    # initial snake coords
    (xs,ys) = (randint(0,1080),randint(0,200))
    Xschange = Yschange = 0

    running = True
    while running:
        screen.blit(pygame.image.load('bg.jpeg'), (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Ychange = -5
                if event.key == pygame.K_DOWN:
                    Ychange = 5
                if event.key == pygame.K_LEFT:
                    Xchange = -5
                if event.key == pygame.K_RIGHT:
                    Xchange = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Ychange = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    Xchange = 0

        x += Xchange
        if (y+Ychange) >= 575: y = 575
        elif (y+Ychange) <= 0: y = 0
        else: y += Ychange

        # update snake coords
        Xschange = randint(-10,10)
        Yschange = randint(0,1)
        xs += Xschange
        ys += Yschange

        snake(xs,ys)
        ladder(x%1000,y)

        pygame.display.update()

game()