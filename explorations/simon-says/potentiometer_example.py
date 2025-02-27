import neopixel
from machine import Pin
import time

LED_COUNT=8
PIXEL_PIN=0
BUTTON_PIN=17
POTENTIOMETER_PIN=26

pix=neopixel.NeoPixel(Pin(PIXEL_PIN), LED_COUNT)
potentiometer=machine.ADC(POTENTIOMETER_PIN)

brightness=.01

red=(int(255*brightness),0,0)
green=(0,int(255*brightness),0)

def loop_pins():
    for i in range(0, LED_COUNT):
        speed=loop_speed()
        pix.fill(red)
        pix[i]=green
        pix.write()
        time.sleep(speed)
        print(f"Sleeping for {speed}")
    pix.fill(red)
    pix.write()

def loop_speed():
    val=potentiometer.read_u16()
    return val/65535.0


myButton=Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
prevState=myButton.value()

while True:
    buttonState=myButton.value()
    if buttonState == 0: # and buttonState != prevState:
        loop_pins()
