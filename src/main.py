import RPi.GPIO as GPIO
import time
import smbus  # comunicación I2C
import math
import pygame


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


distance_thfreshold = 15

#PINOUT
#HC-RS04
#----------
TRIGL = 40
TRIGC = 38
TRIGR = 36

ECHOL = 37
ECHOC = 35
ECHOR = 33

#GY-271
#----------
SCL = 3
SDA = 5

#L298N
#----------
IN1 = 16
IN2 = 18
IN3 = 19
IN4 = 15
ENA = 22
ENB = 23

TIME = 20

GPIO.setmode(GPIO.BOARD)

GPIO.setup(TRIGL,GPIO.OUT)
GPIO.setup(TRIGC,GPIO.OUT)
GPIO.setup(TRIGR,GPIO.OUT)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)
GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(ENB,GPIO.OUT)

GPIO.setup(ECHOL,GPIO.IN)
GPIO.setup(ECHOC,GPIO.IN)
GPIO.setup(ECHOR,GPIO.IN)

def ultrasound(TRIG, ECHO):
    # print("Distance in cm: ")

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
        distance = round(distance, 2)
        print("Distance: %f cm", distance)
        return distance

    except KeyboardInterrupt:
        print("Interrupted")
        GPIO.cleanup()


def movement(dir_obj, dir_robot, obstacles): #obstacles = [right, center, left] (bools) if obstacle or not
    if dir_obj == dir_robot:
        if obstacles[1] == True:
            #go forward
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
        elif obstacles[2] == True:
            #turn right
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
        elif obstacles[0] == True:
            #turn left
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
        else:
            #detenerse
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.LOW)
    else:
        #alinear direccion
        if dir_robot - dir_obj < 0:
            #turn right
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
        elif dir_robot - dir_obj > 0:
            # turn left
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)

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
        heading = heading - 2 * pi
    # revisar el signo
    if (heading < 0):
        heading = heading + 2 * pi
        # convertir a grados
    heading_angle = int(heading * (180 / pi))
    print("angulo = %d°" % heading_angle)
    #sleep(0.5)
    return heading_angle

def call():
    pygame.mixer.init()
    pygame.mixer.music.load("king.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def main():
    start = time.time()
    MagnetometerInit()
    dir_objetivo = 100
    while True:
        dir_robot = accelerometro()
        distances = []
        dist_1 = ultrasound(TRIGR, ECHOR)
        distances.append(dist_1)
        dist_2 = ultrasound(TRIGC, ECHOC)
        distances.append(dist_2)
        dist_3 = ultrasound(TRIGL, ECHOL)
        distances.append(dist_3)
        obstacles = []
        for dist in distances:
            if dist < distance_thfreshold:  # si la distancia en un detector es menor a la minima
                obstacles.append(True)
            else:
                obstacles.append(False)
        movement(dir_objetivo,dir_robot,obstacles)
        end = time.time()
        if end - start > TIME:
            break
    call()

if __name__ == '__main__':
    main()