import neopixel
import random
from machine import Pin
from time import sleep

LED_COUNT=8
PIXEL_PIN=0

GREEN_BUTTON_PIN=14
YELLOW_BUTTON_PIN=7
BLUE_BUTTON_PIN=19
RED_BUTTON_PIN=22

BRIGHTNESS = 0.01
RED=(int(255*BRIGHTNESS),0,0)
GREEN=(0,int(255*BRIGHTNESS),0)
YELLOW=(int(255*BRIGHTNESS),int(255*BRIGHTNESS),0)
BLUE=(0,0,int(255*BRIGHTNESS))
WHITE=(int(255*BRIGHTNESS),int(255*BRIGHTNESS),int(255*BRIGHTNESS))

SUCCESS_GREEN=(int(144*BRIGHTNESS),int(238*BRIGHTNESS),int(144*BRIGHTNESS))
FAILURE_ORANGE=(int(248*BRIGHTNESS),int(152*BRIGHTNESS),int(128*BRIGHTNESS))

class ColorButton:
    def __init__(self, name, button_pin, color_value):
        self.color = color_value
        self.button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        self.name = name

    def is_pressed(self):
        if self.button.value() == 0:
            return True
        return False

pix=neopixel.NeoPixel(Pin(PIXEL_PIN), LED_COUNT)

# Create an object of the button objects and their corresponding color
green_button=ColorButton("green", GREEN_BUTTON_PIN, GREEN)
red_button=ColorButton("red", RED_BUTTON_PIN, RED)
yellow_button=ColorButton("yellow", YELLOW_BUTTON_PIN, YELLOW)
blue_button=ColorButton("blue", BLUE_BUTTON_PIN, BLUE)

all_buttons = [green_button, red_button, yellow_button, blue_button]

def loop_pins():
    for i in range(0, LED_COUNT):
        pix.fill(red)
        pix[i]=green
        pix.write()
        sleep(0.1)
    pix.fill(red)
    pix.write()

def convert_color(from_color, to_color):
    for i in range(0, LED_COUNT):
        pix.fill(from_color)
        for j in range(0,i):
            pix[j]=to_color
        pix.write()
        sleep(0.1)
    pix.fill(to_color)
    pix.write()

def display_pattern(colors):
    pix.fill(WHITE)
    for index, color in enumerate(colors):
        pix[index] = color
    pix.write()

def pressed_buttons():
    pressed = filter(lambda b: b.is_pressed(), all_buttons)
    if pressed == None:
        return []
    return list(pressed)

def flash_result(color):
    pix.fill(color)
    pix.write()
    sleep(0.1)
    pix.fill(WHITE)
    pix.write()

def initialize_game_pattern(length):
    buttons = [green_button, red_button, yellow_button, blue_button]
    choices = []
    for i in range(0, length):
      choices.append(random.choice(buttons))
    return choices

def play_the_game():
    pix.fill(WHITE)
    pix.write()
    pattern = initialize_game_pattern(5)
    color_pattern = [button.color for button in pattern]
    display_pattern(color_pattern)
    sleep(2)
    pix.fill(WHITE)
    pix.write()
    print("Time to play")
    emptyState = True
    for button in pattern:
        print(f"Expecting {button.name}")
        while True:
            pressed = pressed_buttons()
            sleep(0.1)
            if button in (pressed):
                print("Yay")
                emptyState = False
                flash_result(SUCCESS_GREEN)
                break
            if len(pressed) > 0 and emptyState:
                flash_result(FAILURE_ORANGE)
                print("Behrnt")
            emptyState = True
    print("You won!")
    for _ in range(0, 10):
      flash_result(SUCCESS_GREEN)
      sleep(0.1)

play_the_game()
