"""!
@package docstring
Lab 2 - Out of Control

@file position_driver.py
@brief sets the level used by motor_driver.py using kp, the current position, and the end position
@details Defines the level of motor_driver by finding the positional error, then multiplying by kp
"""

class PositionDriver:
    
    def __init__(self):
        """!
        Creates a position driver by initializing kp and end position values in case they are not defined later
        """
        self.kp = 1
        self.setpoint = 256

    def run(self,posnow, setpoint = 8675309, kp = 8675309):
        """!
        Recalculates the error and returns the level used by motor_driver
        @param setpoint End position of the motor
        @param kp 1000x the times of kp
        @returns The level used by motor_driver
        """
        while True:
            if kp != 8675309: self.kp = kp/1000
            if setpoint != 8675309: self.end = setpoint

            self.now = posnow
            self.error = self.end - self.now
            #print(self.error)
            level = self.error * self.kp

            if level > 100:
                level = 100
            elif level < -100:
                level = -100

            yield level

    def set_setpoint(self,setpoint):
        """!
        Resets the end position of the motor to a new value
        @param setpoint End position of the motor
        """
        self.end = setpoint

    def set_kp(self,kp):
        """!
        Resets the kp of the motor to a new value
        @param kp 1000x the times of kp
        """
        self.kp = kp/1000