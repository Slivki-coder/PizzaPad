# PizzaPad
The PizzaPad is a small gadget designed to let you customize and export your pizza orders, while also serving as a fun game to mess around with when you're bored!

The gadget was designed at Hack Club's Undercity Hackathon, held at Github HQ in San Francisco from July 11-14. 

Unfortunately, after countless hours of CAD work, PCB design, and coding a game with only Circuit Python graphics libraries, when we ultimately put the PCB together, we realized that we had fried the Orpheus pico on the board, which made everything obsolete as the board wouldn't even turn on. 

<img src="images/pizzapad">

# PCB
We decided that since this was a handheld device, we should try to make it as compact as possible and that'd be best done with a PCB. I designed a PCB in KiCAD within the constraints of the mill at Undercity. (1 layer, 0.5 mm minimum trace, 0.5 mm minimum distance between traces, etc.). All our breadboard prototyping had worked and we had written the basic functionalities of the game, but in the end we weren't able to make use of the PCB or the device in the form factor we envisioned.

# CAD
Oliver designed a case for the PCB following the constraints of our PCB and only the bottom frame had finished printing in time.

# GAME

The game is quite simple, with players creating their own pizzas and selecting the toppings and amount of toppings they'd like on it. Amounts and types of toppings would be controlled by rotating the encoder, while selecting would be controlled by the encoder's switch. In the end, the goal was to allow the player to export their pizza orders to remember them when they ordered pizza in real life in the future.


# BOM
- 1x Orpheus Pico
- 1x HW-040 Rotary Encoder Switch
- 1x ILI9341 TFT Screen
- 1x 3D Printed Case with 2 parts (only one was printed in time)
- 1x PCB milled by @apr on Slack

