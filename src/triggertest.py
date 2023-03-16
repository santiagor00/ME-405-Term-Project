import pyb,utime
firecount = 0

pinC3 = pyb.Pin(pyb.Pin.board.PC3, pyb.Pin.OUT_PP) #firing pin

on = True
off = not(on)

pinC3.value(off)
"""print("10")
utime.sleep_ms(1000)
print("9")
utime.sleep_ms(1000)
print("8")
utime.sleep_ms(1000)
print("7")
utime.sleep_ms(1000)
print("6")
utime.sleep_ms(1000)
print("5")
utime.sleep_ms(1000)
print("4")
utime.sleep_ms(1000)
print("3")
utime.sleep_ms(1000)
print("2")
utime.sleep_ms(1000)
print("1")
utime.sleep_ms(1000)"""

while firecount < 2:
    try:
        firecount += 1
        print(f"firing {firecount}")
        pinC3.value(on)
        utime.sleep_ms(287)
        pinC3.value(off)
        utime.sleep_ms(1000)
    except KeyboardInterrupt:
        pinC3.value(off)
        print("off")
        break
print("target eliminated")
"""while True:
    try:
        pinC3.value(off)
        print("pain")
        utime.sleep_ms(1000)
        
    except KeyboardInterrupt:
        #pinC3.value(off)
        #print("off")
        break"""