# -*- coding: utf-8 -*-
"""
Created on Tue May 31 23:51:41 2022

@author: rubeg
"""

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