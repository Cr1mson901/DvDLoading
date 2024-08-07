import pygame as py
#Exits after completion
import sys
#Used to get the window
import pygetwindow as gw
#Need to download pywin32
import win32api
import win32con
import win32gui
#Needed for exit key
from pynput import keyboard

import random


with open("config.txt", "r") as c:
    colors = c.readline().split("=")[1].strip().split(",")
    exit_key = c.readline().split("=")[1].strip()
    dimensions = list(map(int, c.readline().split("=")[1].strip().split(",")))
    speed = int(c.readline().split("=")[1].strip())

w, h = dimensions[0], dimensions[1]


# pygame setup
py.init()
#No frame makes it borderless
screen = py.display.set_mode((w, h), py.NOFRAME)
py.display.set_caption("DvD_Logo")
clock = py.time.Clock()
running = True

#Loads the logos in transparent mode
dvds = []
for color in colors:
    dvds.append(py.transform.scale(py.image.load(f'./logos/{color}DvD.png').convert_alpha(),(w,h)))

dvd = random.choice(dvds)


# Getting information of the current active window
hwnd = py.display.get_wm_info()["window"]


# Set the window style to layered and tool window (not showing in the taskbar)
style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

#Sets the window to be transparent
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

#Retrieves the resolution of the screen
screen_full_size =  py.display.get_desktop_sizes()[0]
#Places the logo randomly near the center of the screen
x, y = screen_full_size[0]/2 + random.randint(-250,250), screen_full_size[1]/2 + random.randint(-250,250)

#Get window using pygetwindow
title = "Dvd_Logo"
game_window = gw.getWindowsWithTitle(title)[0]

#X and Y incrementors
x_inc = speed
y_inc = speed

#Global listener for when a key is pressed
def on_press(key):
    global running
    try:
        if key.char == exit_key:
            running = False
    except AttributeError:
        pass

# Start listening for key presses
listener = keyboard.Listener(on_press=on_press)
listener.start()

while running:
    # py.QUIT event means the user clicked X to close your window
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False    

    #Checks if the Image is by the edge of the screen
    if not 0 < y < screen_full_size[1] - h:
        y_inc = y_inc * -1
        dvd = random.choice([i for i in dvds if i != dvd])
    if not 0 < x < screen_full_size[0] - w:
        x_inc = x_inc * -1
        dvd = random.choice([i for i in dvds if i != dvd])
    #Increments and moves the screen
    y += y_inc
    x += x_inc
    game_window.moveTo(int(x), int(y))

    # Ensure the window is always on top
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
    
    #Makes the window Transparent
    screen.fill((0,0,0))

    #Adds the dvd logo to the screen
    screen.blit(dvd,(0,0)) 

    # flip() the display to put your work on screen
    py.display.flip()

    clock.tick(60)  # limits FPS to 60

py.quit()
sys.exit()