import alarm
import board
import displayio
import digitalio
import vectorio
import pwmio

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
        changeArray('left')
    elif btnRight.fell:
        changeArray('right')
    else:
        pass

def splash():
    text = 'Hello\nOllie!'
    newColor()
    text_area = bitmap_label.Label(font=littleFont, text=text, color=color)
    text_area.anchor_point = (0.5, 0.5)
    text_area.anchored_position = (disp_width / 2, disp_height / 2)
    display.root_group = text_area

def buzzBeep():
    pwmBuzzer.duty_cycle = 65500
    sleep(.05)
    pwmBuzzer.duty_cycle = 0

def indexIncDec(upDown):
    global newIndex
    buzzBeep()
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

def changeArray(direction):
    global currentArray
    global newIndex
    global arrId
    buzzBeep()
    newIndex = 0
    if arrId == 1 and direction == 'left':
        arrId = 4
    elif arrId == 4 and direction == 'right':
        arrId = 1
    elif direction == 'left':
        arrId = arrId - 1
    else:
        arrId = arrId + 1
    if arrId == 1:
        currentArray = alphabet
    elif arrId == 2:
        currentArray = numbers
    elif arrId == 3:
        currentArray = shapes
    elif arrId == 4:
        currentArray = colors
    updateDisplay(newIndex)

def shapeBuilder(shape):
    global newShape
    global shapeName
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
    palette[0] = color
    return newShape, shapeName

def newColor():
    global color
    nColor = color
    while nColor == color:
        color = colors[randint(0, 7)][1]
    return color

def bigText(text):
    global text_area
    text_area = bitmap_label.Label(font=bigFont, text=text, color=color)
    text_area.anchor_point = (0.5, 0.5)
    text_area.anchored_position = (disp_width / 2, disp_height / 2)
    return text_area

def littleText(text, bgColor=None):
    global word_area
    if bgColor:
        word_area = bitmap_label.Label(font=littleFont, text=text,
                                       background_color=bgColor, padding_top=30,
                                       padding_bottom=140, padding_right=40,
                                       padding_left=40)
    else:
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
    elif currentArray == shapes:
        newColor()
        shapeBuilder(newIndex)
        noText()
        littleText(shapeName)
        display.root_group = noText_area
        display.root_group.append(newShape)
        display.root_group.append(word_area)
    elif currentArray == colors:
        newColor()
        noText()
        littleText(colors[newIndex][0], colors[newIndex][1])
        display.root_group = noText_area
        display.root_group.append(word_area)
    now = monotonic()

def deepSleep():
    display.brightness = 0
    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)

bigFont = bitmap_font.load_font('fonts/roboto94.pcf')
littleFont = bitmap_font.load_font('fonts/roboto16.pcf')

# arrId 1
alphabet = [('A', 'Apple'), ('B', 'Boat'), ('C', 'Cat'), ('D', 'Dog'),
            ('E', 'Elephant'), ('F', 'Fox'), ('G', 'Grape'), ('H', 'Hat'),
            ('I', 'Inch'), ('J', 'Jump'), ('K', 'Kite'), ('L', 'Ladybug'),
            ('M', 'Mouse'), ('N', 'Nurse'), ('O', 'Owl'), ('P', 'Party'),
            ('Q', 'Queen'), ('R', 'Rose'), ('S', 'Sun'), ('T', 'Tiger'),
            ('U', 'Unicorn'), ('V', 'Vase'), ('W', 'Water'), ('X', 'X-ray'),
            ('Y', 'Yarn'), ('Z', 'Zebra')]
# arrId 2
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
# arrId 3
shapes = ['Square', 'Circle', 'Triangle', 'Rectangle',
          'Diamond', 'Pentagon', 'Star']
# arrId 4
colors = [('Red', 0xF20000), ('Green', 0x00F200), ('Blue', 0x0000F2),
          ('Orange', 0xF26500), ('Yellow', 0xF2F200), ('Purple', 0x8500F2),
          ('Brown', 0x3D1D00), ('Pink', 0xFF00CC)]

display = board.DISPLAY
display.rotation = 180
disp_width = 80
disp_height = 160
display.brightness = 1
palette = displayio.Palette(1)

# Initialize the buttons & pins
btnUp = configBtn(board.GP14)
btnDown = configBtn(board.GP15)
btnLeft = configBtn(board.GP16)
btnRight = configBtn(board.GP17)
pin_alarm = alarm.pin.PinAlarm(board.GP2, value=False, pull=True)
pwmBuzzer = pwmio.PWMOut(board.GP8, duty_cycle=0)


# Start display with splash message, then at alphabet index 0
color = 0xFFFFFF
splash()
sleep(2)
arrId = 1
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
