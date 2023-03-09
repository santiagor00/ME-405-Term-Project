"""!
@package docstring
Lab 2 - Out of Control

@file motor_driver.py
"""

import pyb

class MotorDriver:
    """!
    This class implements a motor driver for an ME405 kit.  
    """
    def __init__(self, enab_pin, in1pin, in2pin, timer):
        """!
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param enab_pin Pin to enable motor power.
        @param in1pin A Pin object, the first PWM pin for the motor input.
        @param in2pin A Pin object, the second PWM pin for the motor input.
        @param timer A Timer object, the timer used for controlling PWM signals to the motor.
        """
        self.enab_pin = enab_pin
        self.in1pin = in1pin
        self.in2pin = in2pin
        self.timer = timer

        self.t3ch1 = timer.channel (1, pyb.Timer.PWM, pin=in1pin)
        self.t3ch2 = timer.channel (2, pyb.Timer.PWM, pin=in2pin)

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        while True:
            level = -level
            self.enab_pin.high()
            
            if level > 0:
                #print("level > 0")
                self.t3ch1.pulse_width_percent(0)
                self.t3ch2.pulse_width_percent(level)
        
            elif level < 0:
                #print("level < 0")
                self.t3ch1.pulse_width_percent(-level)
                self.t3ch2.pulse_width_percent(0)
            
            else:
                self.t3ch1.pulse_width_percent(0)
                self.t3ch2.pulse_width_percent(0)
            #print (f"Setting duty cycle to {level}")
            yield
