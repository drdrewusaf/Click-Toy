import alarm
import board
import displayio
import digitalio
import terminalio

from adafruit_debouncer import Debouncer
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font
from time import sleep
from time import monotonic
from random import randint

def config_btn(pin):
    pin = digitalio.DigitalInOut(pin)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP
    btn = Debouncer(pin)
    return btn

def btnCheck():
    global now
    btnUp.update()
    btnDown.update()
    btnLeft.update()
    btnRight.update()
    if btnUp.fell:
        indexIncDec('up')
    elif btnDown.fell:
        indexIncDec('down')
    elif btnLeft.fell:
        changeArray()
    elif btnRight.fell:
        changeArray()
    else:
        pass

def indexIncDec(upDown):
    global now
    global newIndex
    if upDown == 'up':
        if newIndex + 1 > len(currentArray) - 1:
            newIndex = 0
        else:
            newIndex += 1
    else:
        if newIndex - 1 < 0:
            newIndex = len(currenArray) - 1
        else:
            newIndex -=1
    updateDisplay(newIndex)
    now = monotonic()

def newColor():
    global color
    r = str(hex(randint(0,255))).format(131).split('x')[1]
    g = str(hex(randint(0,255))).format(131).split('x')[1]
    b = str(hex(randint(0,255))).format(131).split('x')[1]
    color = int(f"0x{r}{g}{b}", 16)
    return color

def changeArray():
    global currentArray
    global newIndex
    if currentArray == alphabet:
        currentArray = numbers
    else:
        currentArray = alphabet
    newIndex = 0
    updateDisplay(newIndex)

def updateDisplay(newIndex):
    if currentArray == alphabet:
        text = alphabet[newIndex]
    else:
        text = numbers[newIndex]
    newColor()
    text_area = bitmap_label.Label(font=font, text=text, color=color)
    text_area.anchor_point = (0.5, 0.5)
    text_area.anchored_position = (disp_width / 2, disp_height / 2)
    display.root_group = text_area

def deepSleep():
    text = ' '
    display.brightness = 0
    pwrState = 'off'
    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)

def splash():
    text = 'Hello\nOllie!'
    termFont = terminalio.FONT
    newColor()
    text_area = bitmap_label.Label(font=termFont, text=text, color=color)
    text_area.anchor_point = (0.5, 0.5)
    text_area.anchored_position = (disp_width / 2, disp_height / 2)
    display.root_group = text_area

font_file = "fonts/roboto94.pcf"
font = bitmap_font.load_font(font_file)
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R",
            "S", "T", "U", "V", "W", "X", "Y", "Z"]
numbers = ["1", "2","3","4","5","6","7","8","9","0"]

display = board.DISPLAY
display.rotation = 180
disp_width = 80
disp_height = 160
display.brightness = 1
pwrState = 'on'

#Initialize the buttons
btnUp = config_btn(board.GP14)
btnDown = config_btn(board.GP15)
btnLeft = config_btn(board.GP16)
btnRight = config_btn(board.GP17)
pin_alarm = alarm.pin.PinAlarm(board.GP2, value=False, pull=True)

#Start display with splash message, then at alphabet index 0
splash()
sleep(3)
currentArray = alphabet
newIndex = 0
updateDisplay(newIndex)

while True:
    now = monotonic()
    timeout = now + 120
    while monotonic() < timeout:
        btnCheck()
        timeout = now + 120
    deepSleep()
