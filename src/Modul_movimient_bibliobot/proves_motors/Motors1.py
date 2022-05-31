# -*- coding: utf-8 -*-
"""
Created on Wed May 25 09:41:17 2022

@author: rubeg
"""
#PROVA 1 MOTOR
import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)
Motor1A = 16
Motor1B = 18
Motor1E = 22
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
print("Movimiento hacia delante")
GPIO.output(Motor1A,GPIO.HIGH)
GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor1E,GPIO.HIGH) 
sleep(2)
print("Movimiento hacia atrás")
GPIO.output(Motor1A,GPIO.LOW)
GPIO.output(Motor1B,GPIO.HIGH)
GPIO.output(Motor1E,GPIO.HIGH)
sleep(2)
print("Now stop")
GPIO.output(Motor1E,GPIO.LOW)
GPIO.cleanup()