"""!
@package docstring
Lab 2 - Out of Control

@file encoder_reader.py
"""
import pyb

class EncoderReader:

    """!
    @brief This class is used to read and keep track of the position of an encoder
    """
    
    def __init__(self,enca,encb,tim):

        """!
        @brief Create the EncoderReader

        @param enca Pin object for encoder pin A
        @param encb Pin object for encoder pin B
        @param tim Timer object for for the encoder

        """

        self.encpin1 = enca
        self.encpin2 = encb
        self.timer = tim
        self.tch1 = self.timer.channel (1, pyb.Timer.ENC_AB, pin=enca)
        self.tch2 = self.timer.channel (2, pyb.Timer.ENC_AB, pin=encb)
        
        
        self.encthen = 0
        self.position = 0
        
        self.encnow = 0
        
        


    def zero(self):

        """!
        @brief Reset the position of the encoder to zero

        @returns Current position of the encoder

        """
        
        self.position = 0

    def read(self):

        """!
        @brief Read the current position of the encoder

        @returns Current position of the encoder
        """
        while True:
            self.delt = self.encnow - self.encthen
            self.encthen = self.encnow
            #print("encnow", self.encnow)
            #print("encthen", self.encthen)
            #print("delt", self.delt)
            reset = 32768
            if self.delt > reset:
                self.encthen = self.encnow
                self.delt -= 2*reset
                self.position = self.position + self.delt
            elif self.delt < -reset:
                self.encthen = self.encnow
                self.delt += 2*reset
                self.position = self.position + self.delt
            else:
                self.position = self.position + self.delt
            self.encnow = self.timer.counter()
            yield self.position
    
