"""!
@file main.py
    This file contains the motor control code which runs on the MCU.

@brief Sets up 2 motors and runs motor control tasks.
@details This program contains 3 tasks, two tasks for motor control, and one for reading the camera. The tasks are run based on priority, with the motor control tasks having higher priority.
"""


import gc
import pyb
import cotask
import task_share

import utime
import motor_driver
import encoder_reader
import position_driver
import array
from pyb import repl_uart
from pyb import UART
import mainpage
from machine import I2C


def pinsetup():
    global encreader2, mdriver2, pdriver2, offset
    """
    global ser

    n = 0
    start = "a"
    waiter = 0"""
    """class motor:
        def __init__(self):
            self.kp = 0
            self.endpos = 0
    
    m1 = motor()
    m2 = motor()"""
    """
    repl_uart(None)

    ser = UART(2,115200)
    while start != "start":
        waiter = ser.any()
        while waiter == 0:
            waiter = ser.any()
        startbyte = ser.read(5)
        
        start = startbyte.decode()

        utime.sleep_ms(5)
    
    m1.kp = ser.readline()
    m1.endpos = ser.readline()
    m2.kp = ser.readline()
    m2.endpos = ser.readline()

    m1.kp = m1.kp.decode()
    m1.endpos = m1.endpos.decode()
    m2.kp = m2.kp.decode()
    m2.endpos = m2.endpos.decode()

    m1.kp = m1.kp.strip()
    m1.endpos = m1.endpos.strip()
    m2.kp = m2.kp.strip()
    m2.endpos = m2.endpos.strip()

    m1.kp = int(m1.kp)
    m1.endpos = int(m1.endpos)
    m2.kp = int(m2.kp)
    m2.endpos = int(m2.endpos)"""

    m1kp = 5
    m2kp = 5
    offset = 100000

    tim4 = pyb.Timer (4, prescaler=0, period=0xFFFF)
    tim5 = pyb.Timer (5, freq=20000)

    pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.OUT_PP)
    pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.OUT_PP)

    encreader2 = encoder_reader.EncoderReader(pinB6, pinB7, tim4)

    ENB = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    IN1B = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    IN2B = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    
    ENB.high()

    mdriver2 = motor_driver.MotorDriver(ENB, IN1B, IN2B, tim5)

    pdriver2 = position_driver.PositionDriver()

    level = pdriver2.run(encreader2.read(),offset ,m1kp)

    print("doing a good trick")

    while level > 5:
        posnow = encreader2.read()
        level = pdriver2.run(posnow)
        mdriver2.set_duty_cycle(level)

    print("waiting to picture")
    while utime.ticks_ms() < 5000:
        pass

    target()
    print("target acquired")

    return m1kp,m2kp,sendpos1, sendpos2


def motor1(shares1):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    #print("in motor1")
    # Get references to the share and queue which have been passed to this task
    skp1, sendpos1, finx = shares1

    tim8 = pyb.Timer (8, prescaler=0, period=0xFFFF)
    tim3 = pyb.Timer (3, freq=20000)

    pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.OUT_PP) 
    pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.OUT_PP)
      
    encreader1 = encoder_reader.EncoderReader(pinC6, pinC7, tim8)
      
    ENA = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    IN1A = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    IN2A = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
      
    ENA.high()
      
    mdriver1 = motor_driver.MotorDriver(ENA, IN1A, IN2A, tim3)

    pdriver = position_driver.PositionDriver()

    pdriver.run(encreader1.read(),sendpos1.get() ,skp1.get())

    #timestart = utime.ticks_ms()

    n=0
    nmax=50

    while True:
        posnow = encreader1.read()
        level = pdriver.run(posnow,sendpos1.get())
        mdriver1.set_duty_cycle(level)
        #timenow = utime.ticks_ms()
        if -5 <= level <= 5:
            finx.put(1)
            print("y axis complete")
            """if qtim1.full() == False and qpos1.full() == False:
                qtim1.put(utime.ticks_diff(timenow,timestart))
                qpos1.put(posnow)
                n += 1"""
        else:
            finx.put(0)
            

        #print("end motor1, n=",n)
        yield 0


def motor2(shares2):
    global encreader2, mdriver2, pdriver2
    """!
    Task which turns the base.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    #print("in motor2")
    skp2, sendpos2, finy = shares2

    #timestart = utime.ticks_ms()

    n=0
    nmax=50

    while True:
        posnow = encreader2.read()
        level = pdriver2.run(posnow, setpoint= sendpos2.get())
        mdriver2.set_duty_cycle(level)
        #timenow = utime.ticks_ms()
        if -5 <= level <= 5:
            finy.put(1)
            print("x axis complete")
            """if qtim2.full() == False and qpos2.full() == False:
                qtim2.put(utime.ticks_diff(timenow,timestart))
                qpos2.put(posnow)
                n += 1"""
        else:
            finy.put(0)            
        #print("end motor2, n=",n)"""
        yield 0

def target():
    """!
    Task which sends motor step response test data serially to the computer
    @param shares A tuple of a share and queue from which this task gets data
    """
    #print("in serprint")
    """
    red=3.3v (orange)
    black=gnd (black)
    yellow=scl (brown)
    blue=sda (white)
    """

    """calibration data
    55,81,60,71,53,69,63,91,60,84,41,62,62,80,69,70,57,75,74,77,51,75,55,90,73,64,76,74,74,70,62,73
    27,75,44,53,33,60,48,74,49,64,57,84,45,62,44,74,62,71,48,73,62,50,42,67,75,63,60,76,58,64,63,75
    40,73,55,77,50,77,60,77,67,91,61,78,43,71,63,70,75,63,68,71,64,71,86,76,62,66,69,64,55,62,78,82
    43,71,36,78,48,68,40,84,51,47,41,81,49,56,48,71,38,53,50,66,54,45,57,74,61,69,62,63,49,63,50,74
    49,82,68,97,53,93,76,82,53,78,89,75,51,71,82,83,53,73,71,80,70,62,78,77,77,77,81,71,90,62,83,80
    57,68,41,76,50,80,44,83,43,56,36,80,58,56,49,76,62,66,54,80,44,49,48,82,62,61,74,60,58,43,48,57
    47,94,67,74,61,81,71,99,75,81,95,68,64,82,73,71,76,91,77,63,62,70,81,80,70,82,56,73,76,69,74,60
    42,69,45,64,47,60,53,80,56,63,49,78,66,51,55,69,67,66,54,54,66,55,47,68,60,71,38,76,56,53,41,70
    47,78,53,75,54,91,64,82,60,76,67,84,62,77,63,83,63,75,54,73,70,78,54,68,78,83,81,74,68,81,74,81
    36,64,48,73,61,75,67,67,50,56,40,80,56,58,55,68,54,66,56,50,53,35,43,45,66,61,60,58,44,56,44,68
    54,73,67,73,67,76,58,78,57,84,50,91,69,82,62,86,66,81,61,78,76,70,68,91,64,76,61,80,64,74,58,74
    43,34,69,63,55,47,47,75,41,36,63,81,63,41,68,75,55,49,54,77,67,48,48,69,66,42,41,49,50,43,45,56
    33,56,62,69,38,87,61,80,58,76,67,87,64,82,68,77,60,61,66,77,61,78,56,81,50,82,68,75,50,70,64,68
    51,53,38,67,55,53,38,61,61,42,67,67,55,36,44,66,40,37,50,56,45,37,43,61,56,30,67,49,50,37,47,49
    55,70,56,80,70,77,60,95,47,87,60,76,44,89,67,74,54,66,69,77,42,75,78,77,42,74,64,73,51,78,71,75
    43,61,44,56,37,44,36,86,62,71,30,55,51,44,50,49,51,45,50,76,63,50,58,62,61,56,40,57,44,57,44,51
    40,82,63,60,45,78,58,88,55,80,64,77,61,83,60,67,64,80,56,77,63,90,58,74,57,78,73,74,64,87,76,63
    41,55,30,57,45,60,48,70,49,41,45,53,63,48,51,55,40,44,38,48,49,36,54,40,41,38,31,54,37,41,33,61
    61,56,68,80,55,75,57,86,42,66,54,58,45,82,70,68,57,77,69,64,64,81,67,60,76,71,61,58,58,89,64,55
    37,53,43,61,29,45,53,67,47,54,41,42,27,41,34,57,43,35,47,54,44,42,45,57,45,60,38,43,45,31,50,54
    51,67,60,60,75,58,61,83,43,80,60,73,71,78,68,91,64,61,64,53,56,62,57,81,63,63,60,66,64,44,73,70
    38,58,33,51,45,43,41,67,36,43,30,53,56,45,48,67,33,47,28,42,31,25,57,49,44,40,29,37,49,37,54,33
    38,50,49,60,36,51,53,71,55,69,76,69,55,54,57,64,66,55,67,62,56,49,56,56,50,44,56,63,48,66,63,37
    29,9,27,27,3,18,12,27,18,17,34,18,21,11,33,18,31,18,23,27,22,16,31,22,24,7,27,25,0,10,35,27

    v2

    32,66,54,78,45,77,59,96,56,65,75,70,42,74,56,91,43,56,81,83,60,78,57,77,69,82,69,87,83,83,87,77
    50,66,39,55,45,57,47,66,61,61,42,51,61,46,69,65,45,46,63,63,50,51,54,82,68,69,59,70,75,47,70,66
    43,73,45,99,41,73,64,96,46,59,57,79,41,72,55,91,50,63,61,70,48,81,70,88,63,68,86,88,72,93,77,81
    45,43,33,84,41,34,34,77,59,47,47,75,54,48,64,56,59,69,55,57,48,32,59,56,68,50,57,72,50,48,60,86
    34,73,43,57,47,88,72,93,56,77,54,68,56,78,73,81,55,61,60,77,41,68,59,72,56,81,78,83,64,90,65,78
    50,54,33,72,50,42,41,78,56,48,34,63,39,37,37,84,68,51,50,72,52,38,54,65,60,54,69,81,72,55,59,63
    29,60,47,73,45,69,41,87,61,78,73,78,59,96,81,82,74,77,52,59,60,70,70,61,55,73,55,61,51,64,73,74
    23,50,34,59,52,48,57,65,54,51,46,57,52,68,42,79,55,41,34,63,50,57,50,69,57,39,52,48,55,50,68,55
    25,79,41,65,55,84,66,75,46,70,74,82,65,74,63,82,59,69,64,63,72,87,79,72,52,63,73,65,48,68,64,88
    39,52,46,61,37,60,46,68,42,52,47,70,60,59,51,65,57,64,43,52,57,29,47,48,45,43,57,51,59,39,52,69
    55,82,55,68,41,69,59,73,61,63,63,90,64,73,74,69,52,77,52,79,60,55,68,97,65,84,70,78,60,69,74,88
    47,57,38,65,50,51,56,72,47,50,41,77,57,45,54,68,36,43,33,55,64,48,48,64,51,43,64,57,55,46,45,61
    51,79,33,83,55,82,54,86,61,63,55,82,65,57,72,86,52,78,61,61,52,68,56,96,66,90,63,77,59,82,73,65
    24,51,25,47,27,48,36,77,51,42,56,68,68,54,38,64,52,56,47,57,52,56,48,60,63,54,61,59,52,42,59,42
    29,70,45,72,43,81,56,68,56,74,51,90,54,65,54,82,68,73,60,93,52,60,68,73,57,95,65,83,81,78,54,83
    30,36,39,41,34,36,33,51,42,55,39,61,57,41,54,36,46,25,42,65,60,47,54,61,65,43,60,47,56,65,47,48
    18,50,34,73,36,57,42,78,38,64,64,79,55,43,56,79,56,77,47,92,63,66,60,88,36,73,66,86,61,75,61,91
    23,24,23,37,32,47,45,61,46,37,57,50,55,36,52,48,43,28,51,57,50,28,65,42,39,25,60,51,42,27,61,52
    36,70,33,72,14,52,41,82,41,73,48,82,39,75,43,91,55,79,57,73,59,72,57,88,52,63,70,86,60,81,57,75
    18,46,36,42,15,36,36,39,36,19,30,43,37,38,48,59,23,36,38,47,28,30,36,38,28,38,61,41,32,33,47,48
    38,61,42,59,54,78,43,70,63,51,48,72,52,54,50,82,54,79,65,74,51,63,46,77,48,79,65,77,57,57,63,72
    32,30,24,42,47,42,30,50,29,29,41,37,32,41,18,54,18,25,30,30,34,28,46,27,41,33,29,33,33,23,43,29
    33,51,38,50,27,50,37,56,45,46,50,46,32,48,48,65,29,47,46,75,63,51,54,50,37,60,55,65,55,51,66,55
    15,21,10,18,6,15,1,36,24,19,21,18,15,16,15,10,19,10,10,37,21,28,14,24,9,14,29,25,24,5,23,0
    """
    
    global offset

    i2c = I2C(1, freq=1000000)
    cam = mainpage.MLX_Cam(i2c)
    #refresh rate set as much as possible

    l1 = array.array("i",32*[0])
    l2 = array.array("i",32*[0])
    l3 = array.array("i",32*[0])
    l4 = array.array("i",32*[0])
    l5 = array.array("i",32*[0])
    l6 = array.array("i",32*[0])
    l7 = array.array("i",32*[0])
    l8 = array.array("i",32*[0])
    l9 = array.array("i",32*[0])
    l10 = array.array("i",32*[0])
    l11 = array.array("i",32*[0])
    l12 = array.array("i",32*[0])
    l13 = array.array("i",32*[0])
    l14 = array.array("i",32*[0])
    l15 = array.array("i",32*[0])
    l16 = array.array("i",32*[0])
    l17 = array.array("i",32*[0])
    l18 = array.array("i",32*[0])
    l19 = array.array("i",32*[0])
    l20 = array.array("i",32*[0])
    l21 = array.array("i",32*[0])
    l22 = array.array("i",32*[0])
    l23 = array.array("i",32*[0])
    l24 = array.array("i",32*[0])

    l1c = array.array("i",[55,81,60,71,53,69,63,91,60,84,41,62,62,80,69,70,57,75,74,77,51,75,55,90,73,64,76,74,74,70,62,73])
    l2c = array.array("i",[27,75,44,53,33,60,48,74,49,64,57,84,45,62,44,74,62,71,48,73,62,50,42,67,75,63,60,76,58,64,63,75])
    l3c = array.array("i",[40,73,55,77,50,77,60,77,67,91,61,78,43,71,63,70,75,63,68,71,64,71,86,76,62,66,69,64,55,62,78,82])
    l4c = array.array("i",[43,71,36,78,48,68,40,84,51,47,41,81,49,56,48,71,38,53,50,66,54,45,57,74,61,69,62,63,49,63,50,74])
    l5c = array.array("i",[49,82,68,97,53,93,76,82,53,78,89,75,51,71,82,83,53,73,71,80,70,62,78,77,77,77,81,71,90,62,83,80])
    l6c = array.array("i",[57,68,41,76,50,80,44,83,43,56,36,80,58,56,49,76,62,66,54,80,44,49,48,82,62,61,74,60,58,43,48,57])
    l7c = array.array("i",[47,94,67,74,61,81,71,99,75,81,95,68,64,82,73,71,76,91,77,63,62,70,81,80,70,82,56,73,76,69,74,60])
    l8c = array.array("i",[42,69,45,64,47,60,53,80,56,63,49,78,66,51,55,69,67,66,54,54,66,55,47,68,60,71,38,76,56,53,41,70])
    l9c = array.array("i",[47,78,53,75,54,91,64,82,60,76,67,84,62,77,63,83,63,75,54,73,70,78,54,68,78,83,81,74,68,81,74,81])
    l10c = array.array("i",[36,64,48,73,61,75,67,67,50,56,40,80,56,58,55,68,54,66,56,50,53,35,43,45,66,61,60,58,44,56,44,68])
    l11c = array.array("i",[54,73,67,73,67,76,58,78,57,84,50,91,69,82,62,86,66,81,61,78,76,70,68,91,64,76,61,80,64,74,58,74])
    l12c = array.array("i",[43,34,69,63,55,47,47,75,41,36,63,81,63,41,68,75,55,49,54,77,67,48,48,69,66,42,41,49,50,43,45,56])
    l13c = array.array("i",[33,56,62,69,38,87,61,80,58,76,67,87,64,82,68,77,60,61,66,77,61,78,56,81,50,82,68,75,50,70,64,68])
    l14c = array.array("i",[51,53,38,67,55,53,38,61,61,42,67,67,55,36,44,66,40,37,50,56,45,37,43,61,56,30,67,49,50,37,47,49])
    l15c = array.array("i",[55,70,56,80,70,77,60,95,47,87,60,76,44,89,67,74,54,66,69,77,42,75,78,77,42,74,64,73,51,78,71,75])
    l16c = array.array("i",[43,61,44,56,37,44,36,86,62,71,30,55,51,44,50,49,51,45,50,76,63,50,58,62,61,56,40,57,44,57,44,51])
    l17c = array.array("i",[40,82,63,60,45,78,58,88,55,80,64,77,61,83,60,67,64,80,56,77,63,90,58,74,57,78,73,74,64,87,76,63])
    l18c = array.array("i",[41,55,30,57,45,60,48,70,49,41,45,53,63,48,51,55,40,44,38,48,49,36,54,40,41,38,31,54,37,41,33,61])
    l19c = array.array("i",[61,56,68,80,55,75,57,86,42,66,54,58,45,82,70,68,57,77,69,64,64,81,67,60,76,71,61,58,58,89,64,55])
    l20c = array.array("i",[37,53,43,61,29,45,53,67,47,54,41,42,27,41,34,57,43,35,47,54,44,42,45,57,45,60,38,43,45,31,50,54])
    l21c = array.array("i",[51,67,60,60,75,58,61,83,43,80,60,73,71,78,68,91,64,61,64,53,56,62,57,81,63,63,60,66,64,44,73,70])
    l22c = array.array("i",[38,58,33,51,45,43,41,67,36,43,30,53,56,45,48,67,33,47,28,42,31,25,57,49,44,40,29,37,49,37,54,33])
    l23c = array.array("i",[38,50,49,60,36,51,53,71,55,69,76,69,55,54,57,64,66,55,67,62,56,49,56,56,50,44,56,63,48,66,63,37])
    l24c = array.array("i",[29,9,27,27,3,18,12,27,18,17,34,18,21,11,33,18,31,18,23,27,22,16,31,22,24,7,27,25,0,10,35,27])

    l = [l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17,l18,l19,l20,l21,l22,l23,l24]
    lc = [l1c,l2c,l3c,l4c,l5c,l6c,l7c,l8c,l9c,l10c,l11c,l12c,l13c,l14c,l15c,l16c,l17c,l18c,l19c,l20c,l21c,l22c,l23c,l24c]
    rmax = len(l)*[0]

    scale = 500
    
    while True:
        #print("fin=", fin.get())
        
        if True: #finx.get() == 0 or finy.get() == 0:
            #get image and set positions
            tim1 = utime.ticks_ms()
            image = cam.get_image()
            tim2 = utime.ticks_ms()
            
            o = 0
            for line in cam.get_csv(image, limits=(0, 99)):
                str = line
                sep = str.split(",")

                try:
                    i = 0
                    for n in l1:
                        sep[i] = sep[i].strip()
                        sep[i] = sep[i].strip(" #Aabcdefghijklmnopqrstuvwxyz ")
                        #print(sep[i])
                        l[o][i] = int(sep[i])
                        i+=1
                except ValueError:
                    break
                except IndexError:
                    break
                o+=1
            
            for n in range(len(l)):
                rmax[n] = max(l[n]-lc(n))
            cmax = max(rmax)
            for n in range(len(l)):
                for i in range(len(l[n])):
                    if cmax == l[n][i]:
                        r = n
                        c = i

            if r > 16:
                posx = (r-15)*scale+offset
                #sendpos2.put(posx)
                print("moving left")
            elif r < 15:
                posx = (r-15)*scale+offset
                #sendpos2.put(posx)
                print("moving right")
            else:
                #sendpos2.put(sendpos2.get())  don't uncomment
                print("good x")

            if c > 12:
                posy = 0 #(c-11)*500
                #sendpos1.put(posy)
                print("moving down")
            elif c <11:
                posy = 0
                #sendpos1.put(posy)
                print("moving up")
            else:
                #sendpos1.put(0) don't uncomment
                print("good y")
            print(f"({c},{r}),tim={utime.ticks_diff(tim2,tim1)}ms")

       
        #print("end serprint")
        return sendpos1, sendpos2

def fire(shares):
    #enter code here to fire
    #fire and search again

    finx, finy = shares

    firecount = 0

    pinC3 = pyb.Pin(pyb.Pin.board.PC3, pyb.Pin.OUT_PP) #firing pin

    while True:
        if finx.get() == 1 and finy.get() == 1 and firecount < 2:
            print(f"firing {firecount}")
            firecount += 1
            finx.put(0)
            finy.put(0)
            pinC3.value(0)
            utime.sleep_ms(125)
            pinC3.value(1)
            print("target eliminated")
        yield 0


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    m1,m2,pos1, pos2 = pinsetup()
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    """share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False, name="Queue 0")
    """
    #qtim1 = task_share.Queue('i',300,thread_protect=False,overwrite=False,name="time1")
    #qpos1 = task_share.Queue('i',300,thread_protect=False,overwrite=False,name="position1")
    #qtim2 = task_share.Queue('i',300,thread_protect=False,overwrite=False,name="time2")
    #qpos2 = task_share.Queue('i',300,thread_protect=False,overwrite=False,name="position2")

    skp1 = task_share.Share("i", thread_protect=False, name="shared_kp1")
    sendpos1 = task_share.Share("i",thread_protect=False, name="shared_endpos1")
    skp2 = task_share.Share("i", thread_protect=False, name="shared_kp2")
    sendpos2 = task_share.Share("i",thread_protect=False, name="shared_endpos2")
    finx = task_share.Share("i", thread_protect=False, name="finishedx")
    finy = task_share.Share("i", thread_protect=False, name="finishedy")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    """task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=400, profile=True, trace=False, shares=(share0, q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=1500, profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    """

    skp1.put(m1)
    skp2.put(m2)
    finx.put(0)
    finy.put(0)
    sendpos1.put(pos1)
    sendpos2.put(pos2)

    per = 20
    mot1 = cotask.Task(motor1, name = "motor_1", priority=1, period=per, profile=True, trace=False, shares=(skp1,sendpos1,finx))
    mot2 = cotask.Task(motor2, name = "motor_2", priority=2, period=per, profile=True, trace=False, shares=(skp2,sendpos2,finy))
    arr = cotask.Task(fire, name = "get_image", priority=0, period=per, profile=True, trace=False, shares=(finx,finy))


    cotask.task_list.append(mot1)
    cotask.task_list.append(mot2)
    cotask.task_list.append(arr)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    """print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
    """
