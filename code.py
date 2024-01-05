import alarm
import board
import displayio
import digitalio
import terminalio
import vectorio

from adafruit_debouncer import Debouncer
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
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
    text_area = bitmap_label.Label(font=littleFont, text=text, color=color)
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
            newIndex = len(currentArray) - 1
        else:
            newIndex -= 1
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
    palette[0] = color
    shapeId = shapes[shape]
    if shapeId == 'Square':
        newShape = vectorio.Rectangle(pixel_shader=palette, width=60, height=60, 
                                      x=10, y=50)
        shapeName = 'Square'
    elif shapeId == 'Circle':
        newShape = vectorio.Circle(pixel_shader=palette, radius=30, x=40, y=80)
        shapeName = 'Circle'
    elif shapeId == 'Triangle':
        points = [(10, 110), (40, 50), (70, 110)]
        newShape = vectorio.Polygon(pixel_shader=palette, points=points, x=0, y=0)
        shapeName = 'Triangle'
    elif shapeId == 'Rectangle':
        newShape = vectorio.Rectangle(pixel_shader=palette, width=60, height=90, 
                                      x=10, y=40)
        shapeName = 'Rectangle'
    elif shapeId == 'Diamond':
        points = [(10, 70), (40, 50), (70, 70), (40, 90)]
        newShape = vectorio.Polygon(pixel_shader=palette, points=points, x=0, y=0)
        shapeName = 'Diamond'
    elif shapeId == 'Pentagon':
        points = [(11, 71), (40, 50), (69, 71), (58, 104), (22, 104)]
        newShape = vectorio.Polygon(pixel_shader=palette, points=points, x=0, y=0)
        shapeName = 'Pentagon'
    elif shapeId == 'Star':
        points = [(22, 104), (40, 94), (58, 104), (51, 83), (69, 71), 
                  (47, 71), (40, 50), (33, 71), (11, 71), (29, 83)]
        newShape = vectorio.Polygon(pixel_shader=palette, points=points, x=0, y=0)
        shapeName = 'Star'
    return newShape, shapeName

def newColor():
    global color
    r = str(hex(randint(0, 255))).format(131).split('x')[1]
    g = str(hex(randint(0, 255))).format(131).split('x')[1]
    b = str(hex(randint(0, 255))).format(131).split('x')[1]
    color = int(f'0x{r}{g}{b}', 16)
    return color

def bigText(text):
    global text_area
    text_area = bitmap_label.Label(font=bigFont, text=text, color=color)
    text_area.anchor_point = (0.5, 0.5)
    text_area.anchored_position = (disp_width / 2, disp_height / 2)
    return text_area

def littleText(text):
    global word_area
    word_area = bitmap_label.Label(font=littleFont, text=text, 
                                   background_tight=True)
    word_area.anchor_point = (.5, 1)
    word_area.anchored_position = (disp_width / 2, 30)
    return word_area

def noText():
    global noText_area
    text = ' '
    noText_area = bitmap_label.Label(font=bigFont, text=text, color=color)
    return noText_area

def updateDisplay(newIndex):
    global now
    if currentArray == alphabet:
        letNum = alphabet[newIndex][0]
        word = alphabet[newIndex][1]
        noText()
        bigText(letNum)
        littleText(word)
        newColor()
        display.root_group = noText_area
        display.root_group.append(word_area)
        display.root_group.append(text_area)
    elif currentArray == numbers:
        letNum = numbers[newIndex]
        bigText(letNum)
        newColor()
        display.root_group = text_area
    else:
        newColor()
        shapeBuilder(newIndex)
        noText()
        littleText(shapeName)
        display.root_group = noText_area
        display.root_group.append(newShape)
        display.root_group.append(word_area)
    now = monotonic()

def deepSleep():
    display.brightness = 0
    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)

bigFont = bitmap_font.load_font('fonts/roboto94.pcf')
littleFont = bitmap_font.load_font('fonts/roboto16.pcf')
alphabet = [('A', 'Apple'), ('B', 'Boat'), ('C', 'Cat'), ('D', 'Dog'),
            ('E', 'Elephant'), ('F', 'Fox'), ('G', 'Green'), ('H', 'Hat'), 
            ('I', 'Inch'), ('J', 'Jump'), ('K', 'Kite'), ('L', 'Ladybug'), 
            ('M', 'Mouse'), ('N', 'Nurse'), ('O', 'Owl'), ('P', 'Party'), 
            ('Q', 'Queen'), ('R', 'Rose'), ('S', 'Sun'), ('T', 'Tiger'), 
            ('U', 'Unicorn'), ('V', 'Vase'), ('W', 'Water'), ('X', 'X-ray'), 
            ('Y', 'Yarn'), ('Z', 'Zebra')]
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
shapes = ['Square', 'Circle', 'Triangle', 'Rectangle',
          'Diamond', 'Pentagon', 'Star']

display = board.DISPLAY
display.rotation = 180
disp_width = 80
disp_height = 160
display.brightness = 1
palette = displayio.Palette(1)

# Initialize the buttons
btnUp = configBtn(board.GP14)
btnDown = configBtn(board.GP15)
btnLeft = configBtn(board.GP16)
btnRight = configBtn(board.GP17)
pin_alarm = alarm.pin.PinAlarm(board.GP2, value=False, pull=True)

# Start display with splash message, then at alphabet index 0
splash()
sleep(.1)
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
