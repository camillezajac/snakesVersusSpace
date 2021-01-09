import pygame
import pygame_menu
from math import sqrt, pow
from random import randint

DIFFICULTY = 0
USER = ""
PASS = ""

# graphic sizes:
# lad.png : 64px * 64px
# snk.png : 64px * 64px
# ico.png : 32px * 32px
# bg.jpeg : 1080px * 720px

# initial player coords
(x, y) = (500, 576)

shooting = False

# score
numLaserSnakeCollisions = 0

# player and enemy icons
icon_player = pygame.image.load('lad.png')
icon_snake = pygame.image.load('snk.png')
icon_laser = pygame.image.load('laser.png')

# initialize pygame
pygame.init()

# scoreboard
font = pygame.font.Font('PressStart2P-Regular.ttf', 16)

# display, title and icon
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_icon(pygame.image.load('ico.png'))
pygame.display.set_caption('Snakes vs. Space')

# player
def player(x, y):
    screen.blit(icon_player, (x, y))

# snake
def snake(x, y):
    screen.blit(icon_snake, (x, y))

# laser
def laser(xl, yl):
    global shooting
    shooting = True
    screen.blit(icon_laser, (xl+16, yl+10))

# collision mechanism
def collides(xs, ys, xl, yl):
    D = sqrt(pow(xs-xl,2)+pow(ys-yl,2))
    if D <= 28: return True
    else: return False

# game menu
def menu():
    def set_difficulty(value, difficulty):
        global DIFFICULTY
        DIFFICULTY = difficulty

    def set_user(value):
        global USER
        USER = value

    def set_pass(value):
        global PASS
        PASS = value

    def start_the_game():
        # Do the job here !
        game(DIFFICULTY)

    myimage = pygame_menu.baseimage.BaseImage(
        image_path='bg.jpg',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    pygame_menu.themes.THEME_DARK.background_color = myimage
    pygame_menu.themes.THEME_DARK.widget_font = 'PressStart2P-Regular.ttf'
    pygame_menu.themes.THEME_DARK.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    pygame_menu.themes.THEME_DARK.title_offset = (100,150)
    pygame_menu.themes.THEME_DARK.title_font = 'PressStart2P-Regular.ttf'
    pygame_menu.themes.THEME_DARK.title_font_size = 56
    pygame_menu.themes.THEME_DARK.title_font_color = (124,124,255)
    pygame_menu.themes.THEME_DARK.title_shadow_offset = 10
    pygame_menu.themes.THEME_DARK.title_shadow_color = (255,255,255)

    menu = pygame_menu.Menu(720, 1080, 'Snakes vs. Space', theme=pygame_menu.themes.THEME_DARK)

    # max user length: 16, max password length: 64
    menu.add_text_input('Username: ', onchange=set_user, maxchar=16)
    menu.add_text_input('Password: ', password=True, password_char='*', onchange=set_pass, maxchar=64)
    menu.add_selector('Difficulty: ', [('Easy', 0), ('Medium', 1), ('Hard', 2),], onchange=set_difficulty)
    menu.add_button('Play', game)
    menu.add_button('Quit', pygame_menu.events.EXIT, )

    menu.mainloop(screen)

# game loop
def game():
    space_count = 0
    snk_velocity = [2,3,4]
    global x, y, shooting, numLaserSnakeCollisions
    Xchange = Ychange = 0
    
    # initial snake coords
    snakes = []
    (xs, ys, Xschange, Yschange) = ([],[],[],[])
    
    snakes_count = 4

    for i in range(snakes_count):
        snakes.append(icon_snake)
        xs.append(randint(32, 1048))
        ys.append(randint(0, 200))
        Xschange.append(0)
        Yschange.append(0)


    # (xs, ys) = (randint(0, 1080), randint(0, 200))
    # Xschange = Yschange = 0

    # laser coords
    global xl, yl
    (xl, yl) = (x+16, 576)

    # laser movement
    XLchange = 0
    YLchange = 30
    
    running = True
    while running:
        screen.blit(pygame.image.load('bg.jpg'), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Xchange = -15
                if event.key == pygame.K_RIGHT:
                    Xchange = 15
                if event.key == pygame.K_SPACE:
                    if yl==576:
                        xl = x
                    laser(xl, yl)
                    space_count += 1
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Ychange = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    Xchange = 0
    
            # if snake and player share positon, game is over, need to use dimensions of them for accuracy
            # if (xs, ys) == (x, y):
            #     running = False

            # if snake is shot increase collisions, snake dies (can change as levels get more difficult), create new snake
            # if (xs, ys) == (xl, yl):
            #     numLaserSnakeCollisions += 1
            #     snake(x, y)
    
        if (x + Xchange) >= 1016:
            x = 1016
        elif (x + Xchange) <= 0:
            x = 0
        else:
            x += Xchange

        if (y + Ychange) >= 575:
            y = 575
        elif (y + Ychange) <= 0:
            y = 0
        else:
            y += Ychange
        
        # update snake coords
        for i in range(snakes_count):
            Xsch_rng = randint(-2, 2)
            while (xs[i]+Xsch_rng) < 32 or (xs[i]+Xsch_rng) > 1058:
                Xsch_rng = randint(-2, 2)
            Yschange[i] = randint(0, snk_velocity[DIFFICULTY]) # can change this at number of collisions increases to add difficulty to levels
            xs[i] += Xsch_rng
            ys[i] += Yschange[i]

            if collides(xs[i],ys[i],xl+8,yl+8):
                yl = 576
                shooting = False
                numLaserSnakeCollisions += 5
                
                (xs[i], ys[i]) = (randint(32, 1048), randint(0, 100))

        if yl <= 0:
            yl = 576
            shooting = False
        
        if shooting:
            laser(xl, yl)
            yl -= YLchange

        player(x, y)

        for i in range(snakes_count):
            snake(xs[i], ys[i])
        
        # ui score
        score = font.render(f'Score: {numLaserSnakeCollisions}', True, (0, 255, 0))
        scorebox = score.get_rect()
        scorebox.center = (540, 680)

        # ui player name
        user = font.render(f'Player: {USER}', True, (255, 32, 124))
        userbox = user.get_rect()
        userbox.midleft = (50,680)

        acc_percent = ((numLaserSnakeCollisions/5)/space_count)*100 if space_count != 0 else 0.0

        acc = font.render(f'Accuracy: {round(acc_percent,2)}', True, (255, 32, 124))
        accbox = acc.get_rect()
        accbox.midright = (1030,680)

        screen.blit(pygame.image.load('bar.png'), (0,640))
        screen.blit(user,userbox)
        screen.blit(score,scorebox)
        screen.blit(acc,accbox)

        pygame.display.update()

menu()
