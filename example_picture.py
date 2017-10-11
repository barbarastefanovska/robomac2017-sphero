#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 14:59:54 2017

@author: dimitar
"""

#%% Imports
import pygame
import pygame.camera

#%%
pygame.camera.init()
DEVICE = pygame.camera.list_cameras()[1]  
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
    display.blit(screen,(0,0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            capture = False
camera.stop()
pygame.quit()
