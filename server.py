# This is the program to connect to the android phone that
# the player will be using to control his bot
# Socket Programming is used here where the PC and the Phone connect over a TCP Network

import pygame
import thread
from socket import *

player_controls = [[ pygame.K_LEFT , pygame.K_RIGHT , pygame.K_UP , pygame.K_DOWN ] ,
                       [pygame.K_h, pygame.K_k, pygame.K_u, pygame.K_j],
                       [ pygame.K_a , pygame.K_d , pygame.K_w , pygame.K_s] ,
                       [ pygame.K_c , pygame.K_b , pygame.K_f , pygame.K_v ]
                       ]


ip = ''
port = 0


# To start a thread for the phone controls
# and decipher the messages sent by the phone and allot particular PyGame keys
def start_thread( conn , addr , number ):
    print "Connected By ", addr
    flag = True
    while flag :
        data = conn.recv(1024)
        if "up_pressed" in data:
            event = pygame.event.Event(pygame.KEYDOWN , key= player_controls[number][2])
            pygame.event.post(event)
        elif "down_pressed" in data:
            event = pygame.event.Event(pygame.KEYDOWN , key=player_controls[number][3])
            pygame.event.post(event)
        elif "left_pressed" in data:
            event = pygame.event.Event(pygame.KEYDOWN , key=player_controls[number][0])
            pygame.event.post(event)
        elif "right_pressed" in data:
            event = pygame.event.Event(pygame.KEYDOWN , key=player_controls[number][1])
            pygame.event.post(event)
        elif "up_released" in data:
            event = pygame.event.Event(pygame.KEYUP , key=player_controls[number][2])
            pygame.event.post(event)
        elif "down_released" in data:
            event = pygame.event.Event(pygame.KEYUP , key=player_controls[number][3])
            pygame.event.post(event)
        elif "left_released" in data:
            event = pygame.event.Event(pygame.KEYUP , key=player_controls[number][0])
            pygame.event.post(event)
        elif "right_released" in data:
            event = pygame.event.Event(pygame.KEYUP , key=player_controls[number][1])
            pygame.event.post(event)
        if len(data) > 0:
            pass
        else:
            conn.close()
            flag = False

# Server to connect to the android phone
def connect( ip_add , given_port , players ):
    global ip
    ip = ip_add
    global port
    port = given_port
    s = socket(AF_INET , SOCK_STREAM)
    s.bind( ( ip ,port ) )
    s.listen(players)
    number = 0
    while number < players:
        conn , addr = s.accept()
        thread.start_new_thread( start_thread , ( conn , addr , number ))
        number += 1

    s.close()

