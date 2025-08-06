import board
import displayio
import terminalio
from adafruit_ili9341 import ILI9341
from adafruit_display_text import label
import digitalio
import math
import rotaryio
import time
import busio
import fourwire
import vectorio

displayio.release_displays()

# pin setup - screen
spi = busio.SPI(clock=board.GP21 , MOSI=board.GP19)
tft_cs = board.GP3
tft_dc = board.GP17
tft_rst = board.GP16

# pin setup - encoder
encoder = rotaryio.IncrementalEncoder(board.GP15, board.GP14)
last_position = 0

button = digitalio.DigitalInOut(board.GP13)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  

# display
display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ILI9341(display_bus, width=320, height=240, rotation=90, bgr=True)
main = displayio.Group()
display.root_group = main

# colors
crust_color = 0xf2c78a
sauce_color = 0xe82c3b
cheese_color = 0xe0d690
transparent = 0x000000
bg1 = 0xFF0000
bg2 = 0xF5eb5f
bg3 = 0x145c27

background1 = displayio.Palette(1)
background1[0] = bg1

background2 = displayio.Palette(1)
background2[0] = bg2

background3 = displayio.Palette(1)
background3[0] = bg3

startscreen = displayio.Group()

outer = displayio.Bitmap(display.width, display.height, 1)
inner = displayio.Bitmap(display.width - 40, display.height - 40, 1)

inner_sprite = displayio.TileGrid(inner, pixel_shader=background2, x=20, y=20)
outer_sprite = displayio.TileGrid(outer, pixel_shader=background1, x=0, y=0)

title_group = displayio.Group(scale=3, x=57, y=120)
title_area = label.Label(terminalio.FONT, text="Pizza Game!", color=0xFFFFFF)
title_group.append(title_area)

startscreen.append(outer_sprite)
startscreen.append(inner_sprite)
startscreen.append(title_group)

# start screen
def start():
    main.append(startscreen)
    time.sleep(10)
    main.remove(startscreen)
    
start()

topbg = displayio.Bitmap(display.width, display.height, 1)
toppings_background = displayio.TileGrid(topbg, pixel_shader=background3, x=0, y=0)
main.append(toppings_background)

crust = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=90, x=120, y=120)
crust.pixel_shader[0] = crust_color
main.append(crust)

sauce = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=80, x=120, y=120)
sauce.pixel_shader[0] = sauce_color
main.append(sauce)

cheese = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=75, x=120, y=120)
cheese.pixel_shader[0] = cheese_color
main.append(cheese)

# load bitmaps
pep = displayio.OnDiskBitmap("pepperoni.bmp")
olive = displayio.OnDiskBitmap("olive.bmp")
pine = displayio.OnDiskBitmap("pineapple.bmp")
sausage = displayio.OnDiskBitmap("sausage.bmp")
mush = displayio.OnDiskBitmap("mushroom.bmp")

bmp_list = [pep, olive, pine, sausage, mush]

#toppings
class Topping():
    def __init__(self, bitmap, x, y):         
        self.sprite = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, x=x, y=y)
        self.sprite.pixel_shader.make_transparent(0)
        main.append(self.sprite)

def generateToppings(bitmap): 
    for i in range(12):
        posx = int(115 + 60 * math.cos(math.pi/6 * i)) # convert polar to rect
        posy = int(115 + 60 * math.sin(math.pi/6 * i)) # convert polar to rect
        top = Topping(bitmap, posx, posy)

    for i in range(4):
        posx = int(115 + 15 * math.cos(math.pi/2 * i)) # convert polar to rect
        posy = int(115 + 15 * math.sin(math.pi/2 * i)) # convert polar to rect
        top = Topping(bitmap, posx, posy)
        
    for i in range(8):
        posx = int(115 + 38 * math.cos(math.pi/4 * i)) # convert polar to rect
        posy = int(115 + 38 * math.sin(math.pi/4 * i)) # convert polar to rect
        top = Topping(bitmap, posx, posy)

toppings = ["Pepperoni", "Olive", "Sausage", "Mushroom", "Pineapple"]



# menu
main_label = displayio.Group(scale = 2, x = 210, y = 20)
s1 = label.Label(terminalio.FONT, text="TOPPINGS", color=0xFFFFFF, anchor_point=(0.5, 0.5))
main_label.append(s1)

selected = 0

topping_group = displayio.Group()
for topping in toppings:
    for i, line in enumerate(toppings):
        top = label.Label(
            terminalio.FONT,
            text=line,
            color=0xFFFFFF,
            anchor_point=(0.5, 0.5),
            anchored_position=(260, 80 + i * 20)
        )
        topping_group.append(top)

selector_rectangle = vectorio.Rectangle(pixel_shader = displayio.Palette(1), width=70, height = 3, x=225, y=87)
selector_rectangle.pixel_shader[0] = 0xae1ee3

main.append(main_label)
main.append(selector_rectangle)
main.append(topping_group)


while True:
    # scrolling through menu
    pos = encoder.position
    if pos != last_position:
        diff = pos - last_position
        selected += diff
        selector_rectangle.y += diff * 20
        
    # selecting 
    if not button.value: 
        generateToppings(bmp_list[selected])

        while not button.value:
            time.sleep(0.05)

    time.sleep(0.01)