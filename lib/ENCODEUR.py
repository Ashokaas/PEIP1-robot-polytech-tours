from machine import Pin

# Inverser les pins A et B pour le moteur de gauche

class Encoder:
    def __init__(self, a: str, b: str):
        self.pin_A = Pin(a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pin_B = Pin(b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.A_status = 0
        self.B_status = 0
        self.ticks = 0
        self.pin_A.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, self.Apin)
        self.pin_B.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, self.Bpin)
        
    def Apin(self, arg):
        if arg.value():
            self.A_status = 1
            if self.B_status:
                self.ticks -= 1
            else:
                self.ticks += 1
            
        else:
            self.A_status = 0
            if self.B_status:
                self.ticks += 1
            else:
                self.ticks -= 1
        
    def Bpin(self, arg):
        if arg.value():
            self.B_status = 1
            if self.A_status:
                self.ticks += 1
            else:
                self.ticks -= 1
            
        else:
            self.B_status = 0
            if self.A_status:
                self.ticks -= 1
            else:
                self.ticks += 1