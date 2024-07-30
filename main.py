import pygame as py
#Exits after completion
import sys
#Used to get the window
import pygetwindow as gw
#Need to download pywin32
import win32api
import win32con
import win32gui


#Size of the image
w, h = 140, 140
speed = 2

# pygame setup
py.init()
#No frame makes it borderless
screen = py.display.set_mode((w, h), py.NOFRAME)
py.display.set_caption("DvD_Logo")
clock = py.time.Clock()
running = True

#Loads the logo in transparent mode
blue_dvd = py.image.load('./blueDvD.png').convert_alpha()
blue_dvd = py.transform.scale(blue_dvd,(w,h))

# Getting information of the current active window
hwnd = py.display.get_wm_info()["window"]
#Setting the background to transparent
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                       hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)


screen_full_size = py.display.list_modes()[0]
x, y = screen_full_size[0]/2, screen_full_size[1]/2

#Get window using pygetwindow
title = "Dvd_Logo"
game_window = gw.getWindowsWithTitle(title)[0]

#X and Y incrementors
x_inc = speed
y_inc = speed
while running:
    # py.QUIT event means the user clicked X to close your window
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    
    #Checks if the Image is by the edge of the screen
    if not 0 < y < screen_full_size[1] - h:
        y_inc *= -1
    if not 0 < x < screen_full_size[0] - w:
        x_inc *= -1
    
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
    screen.blit(blue_dvd,(0,0)) 

    # flip() the display to put your work on screen
    py.display.flip()

    clock.tick(60)  # limits FPS to 60

py.quit()
sys.exit()