# -*- coding: utf-8 -*-
"""
Created on Tue May 31 23:56:51 2022

@author: rubeg
"""

def getMicrophoneValues():
    val1 = GPIO.input(MICRO1)
    val2 = GPIO.input(MICRO2)
    val3 = GPIO.input(MICRO3)
    print("Microphone 1 = %i | Microphone 2 = %i | Microphone 3 = %i\n", val1, val2, val3)

def getTimingOfSound():
    time.sleep(2)
    T1 = 0
    T2 = 0
    T3 = 0
    print("waiting for sound")
    while (T1 == 0) | | (T2 == 0) | | (T3 == 0):
        getMicrophoneValues()
        if (T1 == 0) & & (val1 > threshold):
            T1 = micros()
        if (T2 == 0) & & (val2 > threshold):
            T2 = micros()
        if (T3 == 0) & & (val3 > threshold):
            T3 = micros()
    print("T1 = %i | T2 = %i | T3 = %i\n", T1, T2, T3)


#encontrar localizacion de la fuente de sonido
def soundTriangulation():
    getTimingSound()
    A = ((T2 - T1) / 1000000.0) * 343
    B = ((T3 - T1) / 1000000.0) * 343
    a = (math.sqrt(A) + math.sqrt(B))
    b = (((math.sqrt(A) - 1) * A) + ((math.sqrt(B) - 1) * B))
    c = (math.sqrt(math.sqrt(A) - 1) / 4) + (math.sqrt(math.sqrt(B) - 1) / 4)
    T = ((-b - math.sqrt(math.sqrt(b) - (4 * a * c))) / (2 * a))
    X = -((A * T) + ((math.sqrt(A) - 1) / 2))
    Y = -((B * T) + ((math.sqrt(B) - 1) / 2))
    print("A = %0.6f | B = %0.6f\n", A, B)
    print("T = %0.2f\n", T)
    print("X = %0.2f | Y = %0.2f\n", X, Y)
    print("a = %0.2f | b = %0.2f | c = %0.2f\n", a, b, c)
    return X, Y