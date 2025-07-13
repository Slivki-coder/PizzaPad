import math, time, os, random
from machine import Pin, SPI # type: ignore
import ili9341               # type: ignore
import time
from ili9341 import color565 # type: ignore

def draw_noisy_circle(cx, cy, radius, base_color, noise_strength=10):
    r_base, g_base, b_base = base_color

    for y in range(-radius, radius):
        for x in range(-radius, radius):
            if x * x + y * y <= radius * radius:
                r = max(0, min(255, r_base + random.randint(-noise_strength, noise_strength)))
                g = max(0, min(255, g_base + random.randint(-noise_strength, noise_strength)))
                b = max(0, min(255, b_base + random.randint(-noise_strength, noise_strength)))
                display.pixel(cx + x, cy + y, color565(r, g, b))

toppings_graphics = {
    "pepperoni": "graphics/pepperoni.png",
    "mushrooms": "graphics/mushrooms.png",
    "onions": "graphics/onions.png",
    "sausage": "graphics/sausage.png",
    "bacon": "graphics/bacon.png",
    "extra cheese": "graphics/extra_cheese.png",
    "black olives": "graphics/black_olives.png",
    "green peppers": "graphics/green_peppers.png",
    "pineapple": "graphics/pineapple.png",
    "spinach": "graphics/spinach.png"
}

spi = SPI(1, baudrate=40000000, sck=Pin(18), mosi=Pin(19))

display = ili9341.ILI9341(
    spi,
    cs=Pin(17),
    dc=Pin(16),
    rst=Pin(15),
    width=240,
    height=320,
    rotation=0
)

class Pizza:
    def __init__(self):
        self.toppings = {
            "pepperoni": 0,
            "mushrooms": 0,
            "onions": 0,
            "sausage": 0,
            "bacon": 0,
            "extra cheese": 0,
            "black olives": 0,
            "green peppers": 0,
            "pineapple": 0,
            "spinach": 0
        }
        self.current_topping = None
    def add_topping(self, topping, quantity):
        if topping in self.toppings:
            self.toppings[topping] += quantity
        else:
            print(f"Topping {topping} not recognized.")
    def select_topping(self, topping):
        if topping in self.toppings:
            self.current_topping = topping
        else:
            print(f"Topping {topping} not recognized.")
    def increase_topping(self):
        if self.current_topping:
            self.toppings[self.current_topping] += 1
        else:
            print("No topping selected.")
    def decrease_topping(self):
        if self.current_topping:
            if self.toppings[self.current_topping] > 0:
                self.toppings[self.current_topping] -= 1
            else:
                print(f"No {self.current_topping} to remove.")
        else:
            print("No topping selected.")

class Topping:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def draw(self, display):
        color = color565(255, 0, 0) if self.selected else color565(255, 255, 255)
        display.fill_rect(self.x, self.y, 100, 30, color)
        display.text(self.name, self.x + 5, self.y + 5, color565(0, 0, 0))