# @Contributers : Kruti Sutaria (Github: @), Abhinav Sinha (Github: @), Kumar Mallikarjuna (Github: @), Camille Zajac (Github: @camillezajac)

import pygame
from random import randint

# screen dimensions
WIDTH = 1080
HEIGHT = 720

# Upper right : (1080,0)
# Lower left : (0,720)
# Lower right : (1080,720)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#font attributes
size = 25

# unit attributes
# radius
rp = 64# player
rs = 64# snake
rl = 50# laser

# graphic sizes:
# lad.png : 64px * 64px
# snk.png : 64px * 64px
# ico.png : 32px * 32px
# bg.jpeg : 1080px * 720px
# laser.png : 15px * 50px

# initial player coords
(x, y) = (540, 576)

# initial laser coords
(xl, yl) = (540, 576)

# player, enemy, laser
icon_player = pygame.image.load('lad.png')
icon_enemy = pygame.image.load('snk.png')
icon_laser = pygame.image.load('laser.png')

# initialize pygame
pygame.init()

# display, title and icon
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(pygame.image.load('ico.png'))
pygame.display.set_caption('Snakes vs. Space')
font_name = pygame.font.match_font('consolas')

# player
def player(x, y):
    screen.blit(icon_player, (x, y))

# snake
def snake(x, y):
    screen.blit(icon_enemy, (x, y))

# laser
def laser(xl, yl):
    screen.blit(icon_laser, (xl, yl))

# game loop
def game():
    global x, y
    Xchange = Ychange = 0
    
    #font attributes
    size = 25
    score = 0
    text = "Score: " + str(score)

    # initial snake coords
    (xs, ys) = (randint(0, 1080), randint(0, 200))
    Xschange = Yschange = 0

    # initial laser coords
    global xl,yl
    (xl, yl) = (x+23, y-40)
    XLchange = YLchange = 0
    
    running = True
    while running:
        screen.blit(pygame.image.load('bg.jpeg'), (0, 0))
        
        # score keeper text
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
        text_rect = text_surface.get_rect()
        text_rect.midtop = (120, 20)
        screen.blit(text_surface, text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Ychange = -10
                if event.key == pygame.K_DOWN:
                    Ychange = 10
                if event.key == pygame.K_LEFT:
                    Xchange = -10
                if event.key == pygame.K_RIGHT:
                    Xchange = 10
                # laser shooting loop
                if event.key == pygame.K_SPACE:
                        YLchange = -10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Ychange = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    Xchange = 0

            # if snake and player share positon, game is over, need to use collision radius as well
            #or can use built in collision for sprites
            #pygame.org/docs/ref/sprite.html#pygame.sprite.collide_circle_ratio
            if (xs, ys) == (x, y):
                running = False

            # if snake is shot increase collisions, snake dies (can change as levels get more difficult), create new snake
            if (xs, ys) == (xl, yl):
                score += 1
                snake(x, y)
    
        # update laser coords
        #axis offsets on update of laser after dissapearance will be off by a larger and larger amount overtime
        #unless another, instead of offset being an constant, it should update each time
        if (xl, yl) == (x+23, y-40):
            xl += Xchange
            if (yl + Ychange + YLchange) >= 575:
                yl = 575
            elif (yl + Ychange + YLchange) <= 0:
                (xl, yl) = (x + Xchange, y + Ychange + YLchange)
            else:
                yl = yl + Ychange + YLchange
        else:
            if (yl + YLchange) >= 575:
                yl = 575
            elif (yl + YLchange) <= 0:
                (xl, yl) = (x, y + YLchange)
            else:
                yl += YLchange

        # update player coords
        x += Xchange
        if (y + Ychange) >= 615:
            y = 615
        elif (y + Ychange) <= 0:
            y = 0
        else:
            y += Ychange
        
        # update snake coords
        Xschange = randint(-4, 4)
        Yschange = randint(0, 4) #can change this at number of collisions increases to add difficulty to levels
        xs += Xschange
        ys += Yschange

        snake(xs, ys)
        laser(xl, yl)
        player(x % 1000, y)

#        stats(score) # slows it down, only call when updated instead
        pygame.display.update()

game()
