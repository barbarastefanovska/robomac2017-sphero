import cv2
import numpy as np

def red_mask(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower mask (0-10)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
    # upper mask (170-180)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
    # join my masks
    mask = mask0 + mask1
    # dilation: removes spheros' hot zones-zones where movement is forbidden
    # creating a circle kernel
    kernel_circle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    # dilation with a circle kernel
    dilation = cv2.dilate(mask, kernel=kernel_circle, iterations=2)
    # set mask: zero everywhere exept hot zones
    output_img_red = img.copy()
    output_img_red[np.where(dilation == 0)] = 0
    return mask,output_img_red

def blue_mask(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
    # creating a rectangular kernel
    kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    #erosion: locates the center of blue pixels- helps find wanted coordinates
    erosion=cv2.erode(mask,kernel=kernel_rect,iterations=1)
    # set mask: zero everywhere exept target zones
    output_img_blue = img.copy()
    output_img_blue[np.where(mask == 0)] = 0
    return mask,output_img_blue

def green_mask(img):
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #define range of green in hsv
    lower_green = np.array([90, 80, 100])
    upper_green = np.array([180, 100, 100])

    #Treshold the HSV image to get only green colors
    mask=cv2.inRange(img_hsv,lower_green,upper_green)
    #set mask to zero everywhere exept sphero
    output_img_green=img.copy()
    output_img_green[np.where(mask==0)] = 0
    return mask,output_img_green

img=cv2.imread('6.jpg')
cv2.imshow('test image',img)
redmask,output_red = red_mask(img)
bluemask,output_blue=blue_mask(img)
greenmask,output_green=green_mask(img)


cv2.imshow('red mask',redmask)
cv2.imshow('red mask output',output_red)
cv2.imshow('blue mask',bluemask)
cv2.imshow('blue mask output',output_blue)
cv2.imshow('gren mask', greenmask)
cv2.imshow('green mask output',output_green)

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('HSV',img_hsv)

cv2.waitKey(0)
cv2.destroyAllWindows()




