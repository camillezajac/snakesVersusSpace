import time
import pygame
import pygame_menu
import requests
import concurrent.futures
from math import sqrt, pow
from random import randint, randrange


PLAYING = False
DIFFICULTY = 0
SNAKES_COUNT = 3
SHOOTING = False
USER = ""
PASS = ""
TOKEN_GEN = ""


# ~~~~ graphic sizes ~~~~
# laser.png : 32px * 32px
# lad.png : 64px * 64px
# snk.png : 64px * 64px
# ico.png : 32px * 32px
# bg.jpg : 1080px * 720px


# initial player coords
(x, y) = (500, 576)


# background sprite
bg = pygame.image.load('img/bg.jpg')


# player and enemy icons
icon_player = pygame.image.load('img/octocat.png')
icon_snake = pygame.image.load('img/snk.png')
icon_laser = pygame.image.load('img/laser.png')


# initialize pygame
pygame.init()


# scoreboard
font = pygame.font.Font(pygame.font.get_default_font(), 22)


# display, title and icon
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_icon(pygame.image.load('img/ico.png'))
pygame.display.set_caption('Snakes vs. Space')


# get login access and refresh tokens
def gettokens():    
    global USER, PASS
    res = requests.post('https://snakesvsspace.herokuapp.com/api/token/', {"username": USER, "password": PASS}).json()
    print(res)
    return res

def updatedb(user,score,acc,timetaken):
    res = requests.post('https://snakesvsspace.herokuapp.com/scores/', data={"username": user, "accuracy": acc, "score": score, "time_s": timetaken}, headers={"Authorization": f'Bearer {TOKEN_GEN}'}).json()

    print(f'\n"Bearer {TOKEN_GEN}"\n')
    print(res)


# player sprite locator
def player(x, y):
    screen.blit(icon_player, (x, y))


# snake sprite locator
def snake(x, y):
    screen.blit(icon_snake, (x, y))


# laser sprite locator
def laser(xl, yl):
    global SHOOTING
    SHOOTING = True
    screen.blit(icon_laser, (xl+16, yl+10))


# collision mechanism
def collides(xs, ys, xl, yl):
    D = sqrt(pow(xs-xl,2)+pow(ys-yl,2))
    if D <= 28: return True
    else: return False

# main menu
def menu():
    def set_difficulty(value, difficulty):
        global DIFFICULTY
        DIFFICULTY = difficulty

    def set_snakes_count(value, count):
        global SNAKES_COUNT
        SNAKES_COUNT = count

    def set_user(value):
        global USER
        USER = value
        

    def set_pass(value):
        global PASS
        PASS = value
        
    menu_bg = pygame_menu.baseimage.BaseImage(
        image_path='img/bg-menu.jpg',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    menu_bg_creds = pygame_menu.baseimage.BaseImage(
        image_path='img/bg-menu-creds.jpg',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )

    pygame_menu.themes.THEME_DARK.background_color = menu_bg
    pygame_menu.themes.THEME_DARK.widget_font = pygame_menu.font.FONT_MUNRO
    pygame_menu.themes.THEME_DARK.widget_font_size = 36
    pygame_menu.themes.THEME_DARK.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    pygame_menu.themes.THEME_DARK.title_offset = (100,100)

    _menu = pygame_menu.Menu(720, 1080, '', theme=pygame_menu.themes.THEME_DARK) # main menu
    pygame_menu.themes.THEME_DARK.title_offset = (350,100)
    pygame_menu.themes.THEME_DARK.background_color = menu_bg_creds
    _menu_sub = pygame_menu.Menu(720, 1080, '', theme=pygame_menu.themes.THEME_DARK) # credits section menu

    # main menu definition
    # max user length: 16, max password length: 64
    _menu.add_text_input('Username: ', onchange=set_user, maxchar=16)
    _menu.add_text_input('Password: ', password=True, password_char='*', onchange=set_pass, maxchar=64)
    _menu.add_selector('Difficulty: ', [('Easy', 0), ('Medium', 1), ('Hard', 2)], font_color=(204,204,0), onchange=set_difficulty)
    _menu.add_selector('Snakes: ', [('few snakes', 3), ('moderate snakes', 5), ('snakes all day', 6)], font_color=(204,204,0), onchange=set_snakes_count, margin=(0,40))
    _menu.add_button('Play', game, font_color=(144,238,144))
    _menu.add_button('Quit', pygame_menu.events.EXIT, font_color=(255,99,71), margin=(0,40))
    _menu.add_button('Credits', _menu_sub, font_color=(255,51,153))
    

    # credit section menu definition
    _menu_sub.add_button('Abhinav Sinha', pygame_menu.events.NONE, font_color=(255,51,153))
    _menu_sub.add_button('Camille Zajac', pygame_menu.events.NONE, font_color=(255,51,153))
    _menu_sub.add_button('Kruti Sutaria', pygame_menu.events.NONE, font_color=(255,51,153))
    _menu_sub.add_button('Arjun Ojha', pygame_menu.events.NONE, margin=(0,80), font_color=(255,51,153))
    _menu_sub.add_button('www.snakes-vs.space', pygame_menu.events.BACK, font_color=(0,255,255), shadow=True, shadow_color=(255,0,255), shadow_offset=1)

    return _menu


# game loop
def game():
    tokens = gettokens()
    
    if 'refresh' in tokens.keys():
        global TOKEN_GEN
        TOKEN_GEN = tokens['access']
        pass
    else: return
    
    space_count = 0
    SCORE = 0
    finalscore = 0
    snk_velocity = [1.1,1.3,1.7]
    global x, y, SHOOTING
    Xchange = Ychange = 0
    
    # initial snake coords
    snakes = []
    (xs, ys, Xschange, Yschange) = ([],[],[],[])
    
    global SNAKES_COUNT
    for i in range(SNAKES_COUNT):
        snakes.append(icon_snake)
        xs.append(randint(32, 1048))
        ys.append(randint(0, 200))
        Xschange.append(0)
        Yschange.append(0)

    # laser coords
    global xl, yl
    (xl, yl) = (x+16, 570)

    # laser movement
    XLchange = 0
    YLchange = 15
    
    running = True
    start_timer = time.time()
    while running:
        GAME_OVER = False

        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Xchange = -7
                if event.key == pygame.K_RIGHT:
                    Xchange = 7
                if event.key == pygame.K_SPACE:
                    if yl==570:
                        xl = x
                    laser(xl, yl)
                    space_count += 1
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Ychange = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    Xchange = 0
    
        # player x-boundary limit
        if (x + Xchange) >= 1016:
            x = 1016
        elif (x + Xchange) <= 0:
            x = 0
        else:
            x += Xchange
        
        # update snake coords
        for i in range(SNAKES_COUNT):
            if ys[i] >= 550:
                GAME_OVER = True
                break
            Xsch_rng = randint(-2, 2)
            while (xs[i]+Xsch_rng) < 32 or (xs[i]+Xsch_rng) > 1058:
                Xsch_rng = randint(-2, 2)
            Yschange[i] = float(randrange(0, int(100*snk_velocity[DIFFICULTY]))/100) # can change this at number of collisions increases to add difficulty to levels
            xs[i] += Xsch_rng
            ys[i] += Yschange[i]

            if collides(xs[i],ys[i],xl+8,yl+8):
                yl = 570
                SHOOTING = False
                SCORE += 5
                
                (xs[i], ys[i]) = (randint(32, 1048), randint(0, 100))

        # laser resets upon reaching the end
        if yl <= 0:
            yl = 570
            SHOOTING = False
        
        # laser shooting forward
        if SHOOTING:
            laser(xl, yl)
            yl -= YLchange

        # player sprite
        player(x, y)

        for i in range(SNAKES_COUNT):
            snake(xs[i], ys[i])
        
        # return to main menu if game is over
        prevtime = time.time()
        if GAME_OVER:
            stop_timer = time.time()

            go = pygame.font.Font(pygame.font.get_default_font(), 72)

            gameov = go.render('GAME OVER', True, (255, 64, 255))
            gameovbox = gameov.get_rect()
            gameovbox.center = (540, 320)

            finscore = font.render(f'Final Score: {finalscore}', True, (0, 255, 0))
            finscorebox = finscore.get_rect()
            finscorebox.center = (540, 375)

            finacc = font.render(f'Final Accuracy: {round(((finalscore/5)/space_count)*100,2) if space_count != 0 else 0.0}%', True, (0, 255, 0))
            finaccbox = finacc.get_rect()
            finaccbox.center = (540, 400)
            
            fintime = font.render(f'Play Time: {round(stop_timer-start_timer,2)} seconds', True, (0, 255, 0))
            fintimebox = fintime.get_rect()
            fintimebox.center = (540, 425)

            while (time.time()-prevtime) <= 3:
                screen.blit(bg, (0,0))
                screen.blit(gameov,gameovbox)
                screen.blit(finscore,finscorebox)
                screen.blit(finacc,finaccbox)
                screen.blit(fintime,fintimebox)
                pygame.display.update()
            updatedb(USER,SCORE,round(((finalscore/5)/space_count)*100,2),round(stop_timer-start_timer,2))
            
            SCORE = 0
            
            break

        # tracking final score till the game gets over    
        finalscore = SCORE

        # ui score
        score = font.render(f'Score: {SCORE}', True, (0, 255, 0))
        scorebox = score.get_rect()
        scorebox.center = (540, 680)

        # ui player name
        user = font.render(f'Player: {USER}', True, (255,105,180))
        userbox = user.get_rect()
        userbox.midleft = (50,680)

        acc_percent = ((SCORE/5)/space_count)*100 if space_count != 0 else 0.0

        # ui acc
        acc = font.render(f'Accuracy: {round(acc_percent,2)}%', True, (255,105,180))
        accbox = acc.get_rect()
        accbox.midright = (1030,680)
        
        # ui timer
        timer = font.render(f'Time Elapsed: {int(time.time()-start_timer)} sec', True, (255,255,0))
        timerbox = timer.get_rect()
        timerbox.midright = (1030,50)

        screen.blit(pygame.image.load('img/bar.png'), (0,640))
        screen.blit(user,userbox)
        screen.blit(score,scorebox)
        screen.blit(timer,timerbox)
        screen.blit(acc,accbox)

        pygame.display.update()


menu().mainloop(screen)


