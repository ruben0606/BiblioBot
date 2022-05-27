import RPi.GPIO as GPIO
import time
import math
import playsound from playsound
import random
import os
#giroscopio
import smbus  # comunicación I2C
from time import sleep
import math

# direcciones requeridas
# ---------------config
Registro_A = 0x0B
Registro_B = 0x09
RegStatus = 0x06
RegCtrl = 0x09
# ---------------direcciones de la conexión
bus = smbus.SMBus(1)
deviceAdress = 0x0d
# ---------------datos
eje_X_Mag = 0x00
eje_Y_Mag = 0x02
eje_Z_Mag = 0x04
declination = -0.00669
pi = 3.14159265359


GPIO.setmode(GPIO.BCM)

TRIG1 = 15
ECHO1 = 18
TRIG2 = 23
ECHO2 = 24

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

distance_threshold = 7  #distnacia minima a la que se puede acercar el robot a un obstaculo

#detecta obstaculos en el camino
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




#define PINOUT
import curses


#ejecutar movimiento del robot
def movement(objective_position, dir_rob, obstacles): #obstacles = [right, center, left] (bools) if obstacle or not
    dir_robot = accelerometro()
    if objective_position.dir == dir_robot:
        if cent == True:
            #go forward
        elif right == True:
            #turn right
        elif left == True:
            #turn left
        else:
            #dar media vuelta
    else:
        #alinear direccion


"""
    if cent == False:#no puedes pasar
        if right == False:
            if left == False:
                #turn around
            else:
                #turn left
        else:
            #trun rigth
    else:
        #go forward
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

#detectar personas
def vision():



#avisar al culpable
def call():
    #ejecutar primer mp3
    playsound("C:/file_link/file_name")
    # esperar respuesta
    if getMicrophoneValues() == True:
        #contestar con otro mp3
        #file = random.randint(1, 10)  # inclusive
        #playsound("C:/"+ file +"/file_name")

        #random.choice(os.listdir("C:/"))  # change dir name to whatever

def MagnetometerInit():
    # configurar registro A
    bus.write_byte_data(deviceAdress, Registro_A, 0x01)
    # configurar registro B
    bus.write_byte_data(deviceAdress, Registro_B, 0x1D)
    # configurar registro para seleccionar el modo
    # bus.write_byte_data(deviceAdress, ModoRegistro, 0)

def read_raw_data(addr):
    # leer doble byte (16 bits)
    low = bus.read_byte_data(deviceAdress, addr)
    high = bus.read_byte_data(deviceAdress, addr + 1)
    # concatenar los bytes
    valor = ((high << 8) | low)
    # obtener el signo
    if (valor > 32768):
        valor = valor - 65536
    return valor

def accelerometro():
    print('leyendo magnetometro...')
    #while True:
    bandera = bus.read_byte_data(deviceAdress, RegStatus)
    a = "{0:b}".format(bandera)
    if a[len(a) - 1] == 0:
        bandera = bus.read_byte_data(deviceAdress, RegStatus)
    x = read_raw_data(eje_X_Mag)
    y = read_raw_data(eje_Y_Mag)
    z = read_raw_data(eje_Z_Mag)
    heading = math.atan2(y, x) + declination
    # compensar superiores a 360
    if (heading > 2 * pi):
        heading = heding - 2 * pi
    # revisar el signo
    if (heading < 0):
        heading = heading + 2 * pi
        # convertir a grados
    heading_angle = int(heading * (180 / pi))
    print("angulo = %d°" % heading_angle)
    #sleep(0.5)
    return heading_angle


def main():
    MagnetometerInit()
    while True:
        x,y = soundTriangulation()
        dir_obj = atan2(y/x)
        dir_nort = accelerometro()
        dir_nort - dir_obj
        distances = []
        dist_1 = ultrasound(TRIG1, ECHO1)
        distances.append(dist_1)
        dist_2 = ultrasound(TRIG2, ECHO2)
        distances.append(dist_2)
        dist_3 = ultrasound(TRIG3, ECHO3)
        distances.append(dist_3)
        obstacles = []
        for dist in distances:
            if dist < distance_thfreshold:  #si la distancia en un detector es menor a la minima
                obstacles.append(True)
            else:
                obstacles.append(False)
        movement(sound_pos, obstacles)
        while pos != sound_pos:
            distances = []
            obstacles = []
            dist_1 = ultrasound(TRIG1, ECHO1)
            distances.append(dist_1)
            print("distance of DET1 in cm: %f", dist_1)
            dist_2 = ultrasound(TRIG2, ECHO2)
            distances.append(dist_2)
            print("distance of DET2 in cm: %f", dist_2)
            dist_3 = ultrasound(TRIG3, ECHO3)
            distances.append(dist_3)
            print("distance of DET3 in cm: %f", dist_3)
            for dist in distances:
                if dist < distance_thfreshold:  # si la distancia en un detector es menor a la minima
                    obstacles.append(True)
                else:
                    obstacles.append(False)
            movement(sound_pos, obstacles)
        vision()
        call()


if __name__ == "__main__":
    main()



#esperar sonido
#detectar sonido
#calcular origen del sonido
#bucle
    #encarar origen del sonido
    #mirar si hay obstaculos
    #corregir rumbo
#hasta llegar al origen del sonido