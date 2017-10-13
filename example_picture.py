#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 14:59:54 2017

@author: dimitar
"""

#%% Imports
import pygame
import pygame.camera
import masks
import sphero
import numpy as np
import astar
import time
import matplotlib.pyplot as plt
#%%
#sph = sphero.Sphero(
 #       '68:86:E7:07:5A:69')  # connection with the sphero (you should look for the adress in your bluetooth setings)

# %%
#sph.set_rgb(0, 255, 0)  # with this function you can change the colours(RGB) of your sphero

pygame.camera.init()
DEVICE = pygame.camera.list_cameras()[0]
SIZE = (640, 480) 
pygame.init()
pygame.camera.init() # simplest case of opening a camera and capturing a frame as a surface, moreover, the surface called image is whatever the camera was seeing when get_image() was called.
display = pygame.display.set_mode(SIZE, 0) #represents from now on the window on screen; it is a pygame.Surface object (SIZE is the resolution,and 0 are the flags )
camera = pygame.camera.Camera(DEVICE, SIZE) #loads your camera (device is your camera at list 1, size is the resolution)
camera.start() #the camera starts
screen = pygame.surface.Surface(SIZE, 0, display) #pygame object for representing images
capture = True #we going to use this variable to make a infinity while cycle 
while capture:
    screen = camera.get_image(screen)
    img = pygame.surfarray.array3d(screen)
    plt.imshow(screen)
    plt.show()
    display.blit(screen,(0,0))
    pygame.display.flip()
    # %%
    # nmap=
    # path = astar.find_path(nmap, (), (0,0))
    nmap, random_red = masks.red_mask(img)
    print(nmap)
    # cv2.imshow('fig1',nmap)
    nmap = np.array(nmap)
    path = astar.find_path(nmap, (50, 50), (30, 20))
    current = (50, 50)

    for i in range(0, len(path),4):

        nextp = path[i]
        vel = np.sqrt((current[1] - nextp[1]) ** 2 + (nextp[0] - current[0]) ** 2)
        # dev=float(nextp[1]-current[1])/(nextp[0]-current[0])
        alfa = (np.pi) / 2 - (np.arctan2(nextp[1] - current[1], (nextp[0] - current[0])))
        print(alfa)
        alfad = (alfa * 180) / np.pi
        print(alfad)
        if int(alfad) <= 0:
            sph.roll(int(vel), 360 + int(alfad))
        else:
            sph.roll(int(vel), int(alfad))
        time.sleep(1)
        current = nextp
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            capture = False
camera.stop()
pygame.quit()
