import board
import displayio
import terminalio
from adafruit_ili9341 import ILI9341
from adafruit_display_text import label
import digitalio
import rotaryio
import time
import busio
import fourwire

# Release any resources currently in use for the displays
displayio.release_displays()
time.sleep(1)
# Define the SPI bus and pins (adjust as needed for your board)
spi = busio.SPI(clock=board.GP8 , MOSI=board.GP10)
time.sleep(1)
tft_cs = board.GP7
tft_dc = board.GP9
tft_rst = -1

#R


# Create the display bus
display_bus = fourwire.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst
)

# Create the display object
display = ILI9341(display_bus, width=320, height=240, rotation=90)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x0000FF  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)


# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(display.width - 40, display.height - 40, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x5febF5  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)

# Draw a label
text_group = displayio.Group(scale=3, x=57, y=120)
text = "Pizza Game!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
text_group.append(text_area)  # Subgroup for text scaling

# Create a Group to hold the TileGrid
group = displayio.Group()
group.append(bg_sprite)
group.append(inner_sprite)
group.append(text_group)


# Show the group on the display
display.root_group = group
