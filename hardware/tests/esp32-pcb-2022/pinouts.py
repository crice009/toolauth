import asyncio
from machine import Pin, PWM #should this be 'Board' in the new Python?
import neopixel
import countio 
from analogio import AnalogIn



#-------------------------------------------------------------------------
class PCB(object):
    def __init__(self, edition):
        edition = edition

    def __repr__(self):
        return f"PCB({self.edition})"

    def checkConfig(self):
        d = bin(0)
        for sw in self.dips:
            d << 1
            state = sw.value()
            d = d + state
        self.configDec = int(d) #pin 1 is the MSB

    def configMessage(self):    
        d = self.configDec
        if d==0:    #0000 -- pin order: 1234 | sw to the right is a '1'
            self.config="E-Stop | 110VAC S2 Relay | 440VAC 3PH Contactor"
        elif d==1:  #0001
            self.config="E-Stop | 230VAC S2 Relay | 230VAC 3PH Contactor"
        elif d==2:  #0010
            self.config="E-Stop | 230VAC S2 Relay | 230VAC 1PH Contactor"
        elif d==3:  #0011
            self.config="E-Stop | 230VAC S2 Relay | 208VAC 3PH Contactor"
        elif d==4:  #0100
            self.config="E-Stop | 230VAC S2 Relay | 208VAC 1PH Contactor"
        elif d==5:  #0101
            self.config="E-Stop | 110VAC S2 Relay | 110VAC 1PH Contactor"
        elif d==6:  #0110
            self.config="E-Stop | 230VAC S2 Relay | NO S3 Contactor"
        elif d==7:  #0111
            self.config="E-Stop | 110VAC S2 Relay | NO S3 Contactor"
        elif d==8:  #1000
            self.config="NO E-Stop | No S2 relay | <5 Amps doors and switches"
        elif d==9:  #1001
            self.config="NO E-Stop | 110VAC S2 relay | <10 Amps very safe tools"
        elif d==10: #1010
            self.config="invalid DIP switch entry..."
        elif d==11: #1011
            self.config="invalid DIP switch entry..."
        elif d==12: #1100
            self.config="invalid DIP switch entry..."
        elif d==13: #1101
            self.config="invalid DIP switch entry..."
        elif d==14: #1110
            self.config="invalid DIP switch entry..."
        elif d==15: #1111
            self.config="invalid DIP switch entry..."
    
    @asyncio.coroutine
    def setS1Relay(self, delay): #probably a few seconds so members can press the green button
        self.set_s1.ON()
        asyncio.sleep(delay)
        self.set_s1.OFF()

    @asyncio.coroutine
    def tone(self, freq, duration):
        beeper = PWM(self.buzz, freq=freq, duty=512)
        asyncio.sleep(duration)
        beeper.deinit()   

    def getS1Relay(self):
        return self.read_s1.value()

    def getBypass(self):
        bp = self.readBypass.value()
        s1r= self.s1RelayState()
        if bp==0 and s1r==0:
            state=1
        else:
            state=0
        return state

    def getEStop(self): #synchronous
        return self.readEstop()

    def autoEstop(self): #https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/handling-interrupts
        with countio.Counter(self.readEstop) as interrupt:
            if interrupt.count > 0:
                #send some sort of a log that E-Stop was pressed | this may automatically work?
                interrupt.count = 0

    def armEstop(self): #autoEstop and armEstop are my first guess. we'll have to test them...
        asyncio.create_task(self.autoEstop())

    def getCurrentDigital(self): #returns a 1 or 0
        return self.current.digital.value()

    def getCurrentAnalog(self): #returns a float for "percentage measurable current"
        return float((self.current.analog.value * 100) / 65536)

    @asyncio.coroutine
    def setTimeout(self):
        self.timeout.ON()
        asyncio.sleep(0.25)
        self.timeout.OFF()

    @asyncio.coroutine      #as written, this will auto-timeout after 5 minutes of "no tool current" but idk about that digital threshold... needs testing
    def autoTimeout(self):  #this feels like it is ripe for some monads, and more elegance, but idk how to do that...
        asyncio.sleep(5*60)
        if not self.getCurrentDigital():
            self.setTimeout()
            return
        self.autoTimeout()
        return

    @asyncio.coroutine
    def currentUseLogging(self):
        if not self.getEstop(): #will only work with a normal card swipe, until E-Stop is used
            draw = self.getCurrentAnalog()
            #somehow send this to a logging system
            asyncio.sleep(0.1)
            self.currentUseLogging()

#-------------------------------------------------------------------------
#
#       Above we have defined many of the mid-level logic functions
#
#       Below we instantiate the "PCB" to match the physical hardware of the board
#
#-------------------------------------------------------------------------


pcb = PCB("july_2022_CoreyRice")

# All props are set to GPIO pins for ESP32
# devkitc-v4 (board) pins are commented just in case

#SPI communication (with PN532 card reader)
pcb.spi.pico = 23 #[I/O] devkitc_pin_21
pcb.spi.poci = 19 #[I/O] devkitc_pin_27
pcb.spi.sck  = 18 #[I/O] devkitc_pin_28
pcb.spi.cs   =  5 #[I/O] devkitc_pin_29

#I2C communication (with LCD screen or backup for PN532 card reader)
pcb.i2c.sda  = 21 #[I/O] devkitc_pin_25
pcb.i2c.scl  = 22 #[I/O] devkitc_pin_22

#pin to activate Stage 1 relay & begin tool turn-on process 
pcb.set_s1 = Pin(16, Pin.OUT) #devkitc_pin_31 --output
pcb.read_s1 = Pin(17, Pin.IN) #devkitc_pin_30 --intput

#addressable LEDs for user feedback
pixel_pin=15 #devkitc_pin_35
pcb.numPixel = 2 #how many neoPixels
pcb.pixels = neopixel.NeoPixel(pixel_pin, pcb.numPixel, brightness=0.9, auto_write=False)
pcb.pixels.fill((255,0,0))
pcb.pixels.show()

#read state of E-Stop button [LOW means e-stop in use]
pcb.readEstop = Pin(14, Pin.IN) #devkitc_pin_12
pcb.armEstop() #so it will send a log when E-Stop pressed (if it works)

#can be used to shut-off/reset the tool
pcb.timeout = Pin(27, Pin.OUT) # devkitc_pin_11

#check the state of the bypass key
pcb.readBypass = Pin(26, Pin.IN) #devkitc_pin_10
#--------note: only truly bypass if readBypass:LOW && read_s1:LOW

#drive the buzzer for audio feedback
pcb.buzz = Pin(25, Pin.OUT) #devkitc_pin_9
pcb.tone(280, 0.25) #short sound to check it is working

#current sensor to monitor tool use
pcb.current.digital = Pin(35, Pin.IN) #devkitc_pin_6
pcb.current.analog  = AnalogIn(34) #devkitc_pin_5 | values 0-65536

# the dip pins that can give feedback for hardware versions
pcb.dips = [Pin(36, Pin.IN), #1
            Pin(39, Pin.IN), #2
            Pin(32, Pin.IN), #3
            Pin(33, Pin.IN)] #4  |devkitc_pins_vp,vn,32,33
pcb.checkConfig()
pcb.configMessage()