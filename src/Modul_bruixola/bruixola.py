# -*- coding: utf-8 -*-
"""
Created on Tue May 31 23:51:41 2022

@author: rubeg
"""
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
def bruixola():
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
