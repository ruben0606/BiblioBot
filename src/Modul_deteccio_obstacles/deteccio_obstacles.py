# -*- coding: utf-8 -*-
"""
Created on Tue May 31 23:58:24 2022

@author: rubeg
"""

def ultrasound(TRIG, ECHO):
    #print("Distance in cm: ")

    try:
        GPIO.output(TRIG, False)
        print("Waiting to settle sensor")
        time.sleep(0.5)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while True:
        pulse_start = time.time()
        if GPIO.input(ECHO) == GPIO.HIGH:
            break
        while True:
            pulse_end = time.time()
            if GPIO.input(ECHO) == GPIO.LOW:
                break
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance,2)
        #print("Distance: %f cm", distance)
    except KeyboardInterrupt:
        print("Interrupted")
        GPIO.cleanup()
        
    return distance