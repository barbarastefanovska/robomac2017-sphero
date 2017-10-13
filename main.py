#%% Imports
import sphero  #it allows you to conect with your sphero, you have this library in your RBMS folder
import astar
import masks
import cv2
import time
import numpy as np
import pygame.camera
import matplotlib.pyplot as plt



#sph = sphero.Sphero('68:86:E7:07:5A:69')
#sph.set_rgb(0,255,0)

def move(current,path):
    for i in np.linspace(0,len(path),15):

        nextp = path[round(i,0)]
        vel = np.sqrt(((current[1]-nextp[1])*(1/3.69))**2+((nextp[0]-current[0])*(1/3.55))**2)
        alfa = np.pi/2 - (np.arctan2(nextp[1]-current[1],(nextp[0]-current[0])))
        alfad = (alfa*180)/np.pi

        if int(alfad) <= 0:
            sph.roll(int(vel), 360+int(alfad))
        else:
            sph.roll(int(vel), int(alfad))
        time.sleep(1)
        current=nextp

#  camera
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
c = 0


while capture:
    screen = camera.get_image(screen)
    img = pygame.surfarray.array3d(screen)
    print("Image",type(img))
    print("Screen",type(screen))
    display.blit(screen,(0,0))
    pygame.display.flip()
    greenmask = masks.green_mask(img)

    spheroc = masks.sphero_centar(greenmask)
    print(spheroc)
    if c==0:
        bluemask = masks.blue_mask(img)
        one, contours, three = cv2.findContours(bluemask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
        fc = masks.findDot(contours)
        nmap = masks.red_mask(img)
        c=1
    else:
        nmap=masks.red_mask(img)
        nmap=masks.remove_add(img, da, nmap)

    fp,da=masks.find_min_path(spheroc, fc, nmap)
    fp=fp[::-1]



    current = spheroc
    move(current,fp)
    fc = fc.remove(da)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            capture = False
camera.stop()
pygame.quit()

