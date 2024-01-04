import alarm
import board
import displayio
import digitalio
import terminalio

from adafruit_debouncer import Debouncer
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle
#from adafruit_display_shapes.polygon import Polygon
from time import sleep
from time import monotonic
from random import randint

def configBtn(pin):
    pin = digitalio.DigitalInOut(pin)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP
    btn = Debouncer(pin)
    return btn

def btnCheck():
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

def splash():
    text = 'Hello\nOllie!'
    newColor()
    text_area = bitmap_label.Label(scale=2, font=termFont, text=text, color=color)
    text_area.anchor_point = (0.5, 0.5)
    text_area.anchored_position = (disp_width / 2, disp_height / 2)
    display.root_group = text_area
    
def indexIncDec(upDown):
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

def changeArray():
    global currentArray
    global newIndex
    newIndex = 0
    if currentArray == alphabet:
        currentArray = numbers
    elif currentArray == numbers:
        currentArray = shapes
    else:
        currentArray = alphabet
    updateDisplay(newIndex)

def shapeBuilder(shape):
    global newShape
    global shapeName
    newColor()
    shapeId = shapes[shape]
    if shapeId == 'Rect':
        newShape = Rect(10, 50, 60, 60, fill=color)
        shapeName = 'Square'
    elif shapeId == 'Circle':
        newShape = Circle(40, 80, 30, fill=color)
        shapeName = 'Circle'
    elif shapeId == 'Triangle':
        newShape = Triangle(10, 110, 40, 50, 70, 110, fill=color)
        shapeName = 'Triangle'
    return newShape, shapeName

def newColor():
    global color
    r = str(hex(randint(0,255))).format(131).split('x')[1]
    g = str(hex(randint(0,255))).format(131).split('x')[1]
    b = str(hex(randint(0,255))).format(131).split('x')[1]
    color = int(f"0x{r}{g}{b}", 16)
    return color

def updateDisplay(newIndex):
    noText = False
    global now
    if currentArray == alphabet:
        text = alphabet[newIndex]
    elif currentArray == numbers:
        text = numbers[newIndex]
    else:
        shapeBuilder(newIndex)
        noText = True
    if noText:
        text = ' '
        text_area = bitmap_label.Label(font=font, text=text, color=color)
        display.root_group = text_area
        text_area = bitmap_label.Label(font=termFont, text=shapeName, background_tight=True)
        text_area.anchor_point = (.5, 1)
        text_area.anchored_position = (disp_width / 2, 30)
        display.root_group.append(newShape)
        display.root_group.append(text_area)
    else:
        newColor()
        text_area = bitmap_label.Label(font=font, text=text, color=color)
        text_area.anchor_point = (0.5, 0.5)
        text_area.anchored_position = (disp_width / 2, disp_height / 2)
        display.root_group = text_area
    now = monotonic()

def deepSleep():
    text = ' '
    display.brightness = 0
    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)

font_file = "fonts/roboto94.pcf"
font = bitmap_font.load_font(font_file)
termFont = terminalio.FONT
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R",
            "S", "T", "U", "V", "W", "X", "Y", "Z"]
numbers = ["1", "2","3","4","5","6","7","8","9","0"]
shapes = ['Rect','Circle','Triangle']

display = board.DISPLAY
display.rotation = 180
disp_width = 80
disp_height = 160
display.brightness = 1

#Initialize the buttons
btnUp = configBtn(board.GP14)
btnDown = configBtn(board.GP15)
btnLeft = configBtn(board.GP16)
btnRight = configBtn(board.GP17)
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
