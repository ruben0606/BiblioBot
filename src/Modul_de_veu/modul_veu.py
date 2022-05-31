# -*- coding: utf-8 -*-
"""
Created on Tue May 31 23:37:32 2022

@author: rubeg
"""

def call():
    pygame.mixer.init()
    pygame.mixer.music.load("king.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue