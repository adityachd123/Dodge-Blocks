"""
Avishek Santhaliya
BTech Second Year
MNNIT Allahabad.
CSE.
Hello World!! :)
"""

import pygame
import time
import random
import socket
import server

pygame.init()
pygame.display.init()

# Colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
purple = (238 , 130 , 238 )

# Dimensions and other variables
display_height = 500
display_width = 1000
clock = pygame.time.Clock()
FPS = 60

# The Game Variables
blocks = 8
player_size = 10
block_size = 30
bullet_size = 10
fuel_size = 30
level_cross_score = 500
levels = 10
multiplayer = False

# The Game Elements' Colors
text_color = black
block_color = red
bullet_color = black
fuel_color = green
bg_color = white
player_color = blue
player_colors = [ blue , red , yellow , purple ]

# To match the color and return the color codes
def color_match(color):
    if color == "black\n":
        return black
    elif color == "white\n":
        return white
    elif color == "blue\n":
        return blue
    else:
        return white

# To define the variables ( The colors and stuff )
def game_init():
    file = open('Data.txt')
    global bg_color
    global player_color
    color = file.readline()
    bg_color = color_match(color)
    color = file.readline()
    player_color = color_match(color)
    file.close()

# The text method that renders all the text
def display_text( text , color , size ):

    mini_font = pygame.font.SysFont('comicsansms' , 15)
    small_font = pygame.font.SysFont( 'comicsansms' , 25 )
    medium_font = pygame.font.SysFont( 'comicsansms' , 50 )
    large_font = pygame.font.SysFont( 'comicsansms' , 75 )

    if size == "mini":
        text_surface = mini_font.render(text, True, color)
    elif size == "small":
        text_surface = small_font.render( text , True , color )
    elif size == "medium":
        text_surface = medium_font.render( text , True , color )
    elif size == "large":
        text_surface = large_font.render( text , True , color )
    return text_surface

# Method to generate random positions for the blocks and the fuel
def block_gen():
    random_block_y = random.randrange( 0 , display_height - block_size )
    random_block_x = random.randrange( display_width , 2 * display_width )
    return random_block_x , random_block_y

# Method to display Pause Scene
def pause_screen(score):
    screen = pygame.display.get_mode( (display_width,display_height))
    text_surface = display_text("GAME PAUSED", text_color, "small")
    screen.blit(text_surface, (200, 200))
    text_surface = display_text("Press c to continue", text_color, "small")
    screen.blit(text_surface, (200, 250))
    text_surface = display_text("Score : " + str((int)(score)) , red , "small")
    screen.blit(text_surface, (200, 280))
    pygame.display.flip()

    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    flag = False
        clock.tick(FPS)
    return

# Method to display Game Over Scene
def game_over_screen(message , score):

    screen = pygame.display.set_mode( (display_width,display_height))
    screen.fill(bg_color)
    text_surface = display_text(message, red, "small")
    screen.blit(text_surface, (200, 100))
    text_surface = display_text("GAME OVER. Score : " + str((int)(score)), text_color, "small")
    screen.blit(text_surface, (200, 200))
    text_surface = display_text("Press p to play from beginning.", text_color, "small")
    screen.blit(text_surface, (200, 250))
    text_surface = display_text("Press c to start from last check.", text_color, "small")
    screen.blit(text_surface, (200, 275))
    text_surface = display_text("Press m to return to main menu", text_color, "small")
    screen.blit(text_surface, (200, 300))
    pygame.display.update()

    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return 'p'
                elif event.key == pygame.K_m:
                    return 'm'
                elif event.key == pygame.K_c:
                    return 'c'
                elif event.key == pygame.K_q:
                    exit()

        clock.tick(FPS)


# MultiPlayer Game Over Scene
def multi_game_over_screen(message , score):
    screen = pygame.display.set_mode( (display_width,display_height))
    screen.fill(bg_color)
    text_surface = display_text(message, red, "small")
    screen.blit(text_surface, (200, 100))
    text_surface = display_text("Score : " + str((int)(score)), text_color, "small")
    screen.blit(text_surface, (200, 200))
    text_surface = display_text("Press p to play again", text_color, "small")
    screen.blit(text_surface, (200, 250))
    text_surface = display_text("Press m to return to main menu", text_color, "small")
    screen.blit(text_surface, (200, 275))
    pygame.display.update()

    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return 'p'
                elif event.key == pygame.K_m:
                    return 'm'

        clock.tick(FPS)


def bullet_hit( block , bullet ):
    if bullet[0] > block[0] and bullet[0] < block[0] + block_size or bullet[0] + bullet_size > block[0] and bullet[0] + bullet_size < block[0] + block_size:
        if bullet[1] > block[1] and bullet[1] < block[1] + block_size:
            return True
        elif bullet[1] + bullet_size > block[1] and bullet[1] + bullet_size < block[1] + block_size:
            return True

    return False


# ------------To do later ----------------
# To check if any of the blocks or fuel is colliding with each other
def check_parallel():
    # Check all blocks with all blocks and the fuel with all blocks too.
    # If they colllide with each other than remove the block or change the position of the fuel.
    pass
# ------------To do later ----------------


# The main Game Scene
def game_screen( level ):
    points_for_dest_block = (int)( 30 / level )
    extra_oil = (int)( 20 / level )
    dec_oil = 0.3
    points_for_dodging = 1.0 / level
    score = 0
    block_list = []
    i = 0
    while i < blocks:
        block_list.append((block_gen()))
        i += 1

    fuel = block_gen()
    bullet = (-1000,-1000)
    oil = 500
    player_pos_x = player_size * 2
    player_pos_y = display_height / 2

    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Game Screen")
    flag = True
    while flag:
        screen.fill(bg_color)
        text_surface = display_text("LEVEL " + str(level), text_color, "medium")
        screen.blit(text_surface, (250 , 250))
        text_surface = display_text("Press space to begin.", text_color, "small")
        screen.blit(text_surface, (500, 270))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flag = False
        pygame.display.update()

    game_over = False
    game_exit = False
    pos_change_x = 0
    pos_change_y = 0
    action_to_do = 'n'
    while not game_exit:
        screen.fill(bg_color)
        text_surface = display_text("Score : " + str((int)(score)), text_color, "mini")
        screen.blit( text_surface , (0,0))
        text_surface = display_text("Oil : " + str((int)(oil)), text_color, "mini")
        screen.blit(text_surface, (100, 0))
        # For controlling the player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pos_change_y = -player_size
                    pos_change_x = 0
                elif event.key == pygame.K_DOWN:
                    pos_change_y = player_size
                    pos_change_x = 0
                elif event.key == pygame.K_LEFT:
                    pos_change_x = -player_size
                    pos_change_y = 0
                elif event.key == pygame.K_RIGHT:
                    pos_change_x = player_size
                    pos_change_y = 0
                elif event.key == pygame.K_p:
                    pause_screen(score)
                elif event.key == pygame.K_SPACE :
                    if bullet == ( -1000 , -1000 ):
                        bullet = ( player_pos_x , player_pos_y )

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    pos_change_y = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    pos_change_x = 0

        if( 0 <= player_pos_y + pos_change_y <= display_height-player_size ):
            player_pos_y += pos_change_y
        if (0 <= player_pos_x + pos_change_x <= display_width - player_size):
            player_pos_x += pos_change_x

        # To generate the blocks
        j = 0
        while j < blocks :
            block = block_list[0]
            del block_list[0]
            pygame.draw.rect( screen , block_color , [block[0] ,block[1] , block_size , block_size] )
            if bullet_hit( block , bullet ):
                block_list.append((block_gen()))
                score += points_for_dest_block
                bullet = ( -1000 , -1000 )
            elif block[0]-(block_size/3) >= 0:
                block_list.append( ( block[0]-block_size/3 , block[1] ) )
            else:
                block_list.append((block_gen()))
            j += 1

        # To generate bullet
        if bullet == ( -1000 , -1000 ):
            pass
        else :
            if( bullet[0] + (bullet_size/3) >= display_width):
                bullet = ( -1000 , -1000 )
            else :
                bullet = ( bullet[0] + (bullet_size/3) , bullet[1] )
            pygame.draw.rect(screen, bullet_color, [bullet[0], bullet[1], bullet_size, bullet_size])

        # To generate fuel
        pygame.draw.rect( screen , fuel_color , [ fuel[0] , fuel[1] , fuel_size , fuel_size ] )
        if(fuel[0] - (fuel_size/3) >= -500 ):
            fuel = ( fuel[0] - (fuel_size/3),fuel[1])
        else:
            fuel = block_gen()

        # To check if the player has hit the blocks
        for block in block_list:
            if player_pos_x > block[0] and player_pos_x < block[0] + block_size or player_pos_x + player_size >  block[0] and player_pos_x + player_size < block[0] + block_size:
                if player_pos_y > block[1] and player_pos_y < block[1] + block_size :
                    action_to_do = game_over_screen("Sorry Loser! You hit a Block.",score)
                elif player_pos_y + player_size > block[1] and player_pos_y + player_size < block[1] + block_size:
                    action_to_do = game_over_screen("Sorry Loser! You hit a Block.",score)

        # To check if the player takes the fuel
        if player_pos_x > fuel[0] and player_pos_x < fuel[0] + fuel_size or player_pos_x + player_size > fuel[0] and player_pos_x + player_size < fuel[0] + fuel_size:
            if player_pos_y > fuel[1] and player_pos_y < fuel[1] + fuel_size:
                fuel = ( 0-fuel_size, 0)
                oil += extra_oil
            elif player_pos_y + player_size > fuel[1] and player_pos_y + player_size < fuel[1] + fuel_size:
                fuel = ( 0-fuel_size, 0)
                oil += extra_oil
        if oil <= 0 :
            action_to_do = game_over_screen("Sorry Bro! Fuel Over. Better luck next time!" ,score)
        score += points_for_dodging
        if score > level_cross_score:
            action_to_do = 'd'
        oil -= dec_oil
        pygame.draw.rect( screen , player_color , [ player_pos_x , player_pos_y , player_size , player_size] )
        pygame.display.update()
        if action_to_do != 'n':
            return action_to_do
        clock.tick(FPS)


# Method to display the Multi PLayer Game Screen.
def multi_game_screen( level , players ):

    # Left , right , up , down
    player_controls = [[ pygame.K_LEFT , pygame.K_RIGHT , pygame.K_UP , pygame.K_DOWN ] ,
                       [pygame.K_h, pygame.K_k, pygame.K_u, pygame.K_j],
                       [ pygame.K_a , pygame.K_d , pygame.K_w , pygame.K_s] ,
                       [ pygame.K_c , pygame.K_b , pygame.K_f , pygame.K_v ]
                       ]
    points_for_dest_block = (int)(30 / level)
    extra_oil = (int)(20 / level)
    dec_oil = 0.3
    points_for_dodging = 1.0 / level
    score = []
    oil = []
    block_list = []
    i = 0
    while i < blocks:
        block_list.append((block_gen()))
        i += 1

    fuel = block_gen()
    #bullet = (-1000, -1000)
    player_pos_x = []
    player_pos_y = []
    player_game_over = []
    for i in range(1,players):
        player_pos_x.append(player_size * 2)
        player_pos_y.append(display_height / ( 4 * i ) )
        score.append(0)
        oil.append(500)
        player_game_over.append(False)

    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("MultiPlayer Game Screen")
    flag = True

    game_over = False
    game_exit = False
    pos_change_x = []
    pos_change_y = []
    for i in range(1,players):
        pos_change_x.append(0)
        pos_change_y.append(0)

    action_to_do = 'n'
    while not game_exit:

        screen.fill(bg_color)
        pos = 0
        i = 0
        j = 0
        for val in player_game_over:
            if val:
                i += 1
            else:
                pos = j
            j+= 1
        if  i == players - 2  :
            action_to_do = multi_game_over_screen("Player " + str(pos+1) + " wins." , score[j-1] )

        # For controlling the players
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                j = 0
                for control in player_controls:
                    i = 1
                    for key in control:
                        if event.key == key:
                            if i == 1:
                                pos_change_x[j] = -player_size
                                pos_change_y[j] = 0
                            elif i == 2:
                                pos_change_x[j] = player_size
                                pos_change_y[j] = 0
                            elif i == 3:
                                pos_change_y[j] = -player_size
                                pos_change_x[j] = 0
                            elif i == 4:
                                pos_change_y[j] = player_size
                                pos_change_x[j] = 0
                        i += 1
                    j += 1
                    if j == players:
                        break

                if event.key == pygame.K_p:
                    pause_screen(score)

            if event.type == pygame.KEYUP:
                j = 0
                for control in player_controls:
                    i = 1
                    for key in control:
                        if event.key == key:
                            if i == 1 or i == 2:
                                pos_change_x[j] = 0
                            elif i == 3 or i == 4:
                                pos_change_y[j] = 0
                        i += 1
                    j += 1
                    if j == players:
                        break

        i = 0
        for x , y in zip(player_pos_x , player_pos_y):
            if (0 <= y + pos_change_y[i] <= display_height - player_size):
                player_pos_y[i] += pos_change_y[i]
            if (0 <= x + pos_change_x[i] <= display_width - player_size):
                player_pos_x[i] += pos_change_x[i]
            i += 1

        # To generate the blocks
        j = 0
        while j < blocks:
            block = block_list[0]
            del block_list[0]
            pygame.draw.rect(screen, block_color, [block[0], block[1], block_size, block_size])
            if block[0] - (block_size / 3) >= 0:
                block_list.append((block[0] - block_size / 3, block[1]))
            else:
                block_list.append((block_gen()))
            j += 1

        # To generate fuel
        pygame.draw.rect(screen, fuel_color, [fuel[0], fuel[1], fuel_size, fuel_size])
        if (fuel[0] - (fuel_size / 3) >= -500):
            fuel = (fuel[0] - (fuel_size / 3), fuel[1])
        else:
            fuel = block_gen()

        # To check if the player has hit the blocks
        i = 1
        for x , y in zip(player_pos_x , player_pos_y):
            for block in block_list:
                if x > block[0] and x < block[0] + block_size or x + player_size > block[0] and x + player_size < block[0] + block_size:
                    if y > block[1] and y < block[1] + block_size:
                        player_game_over[i-1] = True
                    elif y + player_size > block[1] and y + player_size < block[1] + block_size:
                        player_game_over[i - 1] = True

            i += 1

        # To check if the player takes the fuel
        i = 0
        for x , y in zip( player_pos_x , player_pos_y) :
            if x > fuel[0] and x < fuel[0] + fuel_size or x + player_size > fuel[0] and x + player_size < fuel[0] + fuel_size:
                if y > fuel[1] and y < fuel[1] + fuel_size:
                    fuel = (0 - fuel_size, 0)
                    oil[i] += extra_oil
                elif y + player_size > fuel[1] and y + player_size < fuel[1] + fuel_size:
                    fuel = (0 - fuel_size, 0)
                    oil[i] += extra_oil

            i += 1

        for i in range(0,players-1):
            if oil[i] <= 0:
                player_game_over[i] = True
                #action_to_do = game_over_screen("Sorry Bro! Fuel Over. Better luck next time!", score)
            score[i] += points_for_dodging

        #if score > level_cross_score:
        #    action_to_do = 'd'
        for i in range( 0 , players-1 ):
            oil[i] -= dec_oil
        i = 0
        for x , y in zip(player_pos_x , player_pos_y ):
            if not player_game_over[i] :
                pygame.draw.rect(screen, player_colors[i], [x, y, player_size, player_size])
                text_surface = display_text("Score " + str(i+1) + " : " + str((int)(score[i])), text_color, "mini")
                screen.blit(text_surface, (0, 20 * i))
                text_surface = display_text("Oil " + str(i+1) + " : " + str((int)(oil[i])), text_color, "mini")
                screen.blit(text_surface, (100, 20 * i))
            i += 1

        pygame.display.update()
        if action_to_do != 'n':
            return action_to_do
        clock.tick(FPS)

# Method that displays Help Scene
def help_screen():
    screen = pygame.display.set_mode((display_width,display_height))
    screen.fill(bg_color)
    text_surface = display_text("Rules.", ( 90 , 50 , 200), "large")
    screen.blit(text_surface, (200, 100))
    text_surface = display_text("1. Dodge the blocks that are coming to hit you." , red , "mini")
    screen.blit( text_surface, (200 , 230) )
    text_surface = display_text("2. Use the arrow keys to move your spaceship and space to shoot a bullet.", red , "mini")
    screen.blit(text_surface, (200, 250))
    text_surface = display_text("3. Remember, there can be only one bullet on the screen at one moment.", red , "mini")
    screen.blit(text_surface, (200, 270))
    text_surface = display_text("4. You get points for dodging blocks and destroying blocks as well.",red, "mini")
    screen.blit(text_surface, (200, 290))
    text_surface = display_text("5. Score " + str( level_cross_score) + " Points to cross each level. Level difficulty keeps on increasing.", red, "mini")
    screen.blit(text_surface, (200, 310))
    text_surface = display_text("5. There are " + str(levels) + " levels at present.", red, "mini" )
    screen.blit(text_surface, (200, 330))
    text_surface = display_text("Lets see if you can beat the high score.", text_color, "small")
    screen.blit(text_surface, (200, 380))
    text_surface = display_text("Press r to return to main menu.", text_color, "small")
    screen.blit(text_surface, (200, 420))
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    flag = False
        pygame.display.update()

    start_screen()

# To shop new things.
def shop_screen():
    file = open('Data.txt')
    color1 = file.readline()
    color2 = file.readline()
    screen = pygame.display.set_mode( (display_width,display_height) )
    pygame.display.set_caption("Shop.")
    screen.fill( white )
    text_surface = display_text("SHOP", (94,94,0) , "large")
    screen.blit(text_surface, (150, 20))
    text_surface = display_text("Press b to change game background.", text_color , "small")
    screen.blit(text_surface, (150, 120))
    text_surface = display_text("Press p to change player color.", text_color, "small")
    screen.blit(text_surface, (150, 150))
    text_surface = display_text("Press m to return to main menu.", text_color, "small")
    screen.blit(text_surface, (150, 180))
    text_surface = display_text("Present Player Color -> " + color2[:-1] , text_color, "mini")
    screen.blit(text_surface, (150, 250))
    text_surface = display_text("Present Background Color -> " + color1[:-1], text_color, "mini")
    screen.blit(text_surface, (150, 280))
    pygame.display.update()
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    # Put bg_color change here
                    pass
                elif event.key == pygame.K_p:
                    # Put player_color change here
                    pass
                elif event.key == pygame.K_m:
                    flag = False
    file.close()

# Congratualting Screen ( Yaha tak pahuch ke dikha dey koi bhi, hack ke bina :p )
def congo_screen():
    screen = pygame.display.set_mode(( display_width , display_height ))
    pygame.display.set_caption("Congratulations")
    while True:
        screen.fill(bg_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_q:
                    exit()
        text_surface = display_text("You're a Hero. Love You!", ( 50 , 150 , 100) , "medium")
        screen.blit(text_surface, (150, 100))
        text_surface = display_text("Was a kids game though :p ", (50, 150, 100), "medium")
        screen.blit(text_surface, (150, 150))
        text_surface = display_text("Press Space to return to Main Menu.", ( 45 , 170 , 89 ) , "small")
        screen.blit(text_surface, (150, 220))
        text_surface = display_text("Press q to Quit Game.", ( 80 , 0 , 99) , "small")
        screen.blit(text_surface, (150, 250))
        text_surface = display_text("Keep on playing and also ask your friends to :) ", (80, 0, 99), "small")
        screen.blit(text_surface, (150, 280))

        pygame.display.update()

# Method to add a high score to the list
def add_high_score( name , level ):
    file = open('HighScores.txt' , 'r')
    high_scores = file.readlines()
    new_score = name + " " + str(level) + "\n"
    for high_score in high_scores:
        if new_score == high_score:
            return
    file.close()
    file = open('HighScores.txt' , 'a+')
    file.write(new_score)
    file.close()


# Method to display the high scores of the players
def high_score_screen():
    file = open('HighScores.txt')
    screen = pygame.display.set_mode( (display_width , display_height ))
    screen.fill( white )

    text_surface = display_text("High Scores.", ( 69 , 150 , 20 ), "medium")
    screen.blit(text_surface, (150, 10))
    text_surface = display_text("Press r to return to Main Menu.", (69, 150, 20), "mini")
    screen.blit(text_surface, (150, 400))
    high_scores = file.readlines()
    i = 80
    for high_score in high_scores:
        text_surface = display_text( high_score[:-1] , text_color , "mini" )
        screen.blit( text_surface , (150 , i))
        i += 20
    pygame.display.update()

    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    flag = False
    file.close()

# To ask the users for multiplayer or single.
def game_type():
    flag = True
    global multiplayer
    multiplayer = False
    screen = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption("How many?")
    while flag:
        screen.fill(bg_color)
        text_surface = display_text("m for multiplayer s for solo", text_color, "medium")
        screen.blit(text_surface, (250, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    multiplayer = True
                    flag = False
                elif event.key == pygame.K_s:
                    flag = False
        pygame.display.update()

def connection_screen(players):
    #Enter the IP Address of your PC here
    ip = "192.168.0.3"
    port = 12456
    screen = pygame.display.set_mode((display_width,display_height))
    screen.fill( bg_color )
    pygame.display.set_caption('Connect all players')
    text_surface = display_text("All 4 connect to " + ip + " : " + str(port),  (100, 0, 50), "small")
    screen.blit(text_surface, (100, 50))
    text_surface = display_text("After all players connected, press space to begin", (100, 0, 50), "small")
    screen.blit(text_surface, (100, 100))
    pygame.display.update()
    server.connect( ip, port , players )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return



# Method to display Main Menu
def start_screen():
    game_init()

    flag = True
    while flag:
        screen = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("Sanvas Game")

        screen.fill((192, 192, 192))
        text_surface = display_text("Sanvas Game", (100, 0, 50), "medium")
        screen.blit(text_surface, (200, 150))
        text_surface = display_text("Press p to play q to quit and h for help", text_color, "small")
        screen.blit(text_surface, (200, 210))
        text_surface = display_text("During the Game Press p to pause", text_color, "small")
        screen.blit(text_surface, (200, 250))
        text_surface = display_text("Press s to shop adavnces.", text_color, "small")
        screen.blit(text_surface, (200, 290))
        text_surface = display_text("Press z to see high scores.", text_color, "small")
        screen.blit(text_surface, (200, 330))
        text_surface = display_text("Developed with <3 by avisheksanvas.", (10, 100, 100), "small")
        screen.blit(text_surface, (500, 390))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_type()
                    if multiplayer :
                        #Enter number of players here.
                        players = 4
                        connection_screen(players)
                        while True:
                            c = multi_game_screen( 1 , players+1 )
                            if c == 'p':
                                pass
                            else:
                                break

                    else:
                        i = 1
                        while i <= levels :
                            c = game_screen(i)
                            if c == 'm':
                                break
                            elif c == 'd' :
                                i += 1
                            elif c == 'p' :
                                i = 1
                            elif c == 'c' :
                                pass
                        if i == levels+1:
                            congo_screen()
                        name = "Avishek"
                        if i > 1 :
                            add_high_score(name, i-1)
                elif event.key == pygame.K_h:
                    help_screen()
                elif event.key == pygame.K_s:
                    shop_screen()
                elif event.key == pygame.K_z:
                    high_score_screen()
                elif event.key == pygame.K_q:
                    exit()


# The main function
def main():
    start_screen()

if __name__ == "__main__" :
    main()




