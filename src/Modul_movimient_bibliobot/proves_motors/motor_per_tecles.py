# -*- coding: utf-8 -*-
"""
Created on Tue May 31 23:36:36 2022

@author: rubeg
"""

import curses
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

def main(letra):
    while True:
        curses.halfdelay(1)
        key = letra.getch()
        #print key
        if key == 113:
            break
        elif key == 119:
            print "adelante"
            GPIO.output(20, GPIO.LOW)
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(19, GPIO.LOW)
            GPIO.output(16, GPIO.HIGH)
        elif key == 97:
            print "izquierda"
            GPIO.output(20, GPIO.LOW)
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(19, GPIO.HIGH)
            GPIO.output(16, GPIO.LOW)
        elif key == 115:
            print "atras"
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(19, GPIO.HIGH)
            GPIO.output(16, GPIO.LOW)
        elif key == 100:
            print "derecha"
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(19, GPIO.LOW)
            GPIO.output(16, GPIO.HIGH)
        else:
            print "detenido"
            GPIO.output(20, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            GPIO.output(19, GPIO.LOW)
    
curses.wrapper(main)
GPIO.cleanup()