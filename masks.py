import cv2
import numpy as np
import astar

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
    kernel_circle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    # dilation with a circle kernel
    dilation = cv2.dilate(mask, kernel=kernel_circle, iterations=2)
    # set mask: zero everywhere exept hot zones
    output_img_red = img.copy()
    output_img_red[np.where(dilation == 0)] = 0
    return mask #, output_img_red

def blue_mask(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([120, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
    # creating a rectangular kernel
    kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    #erosion: locates the center of blue pixels- helps find wanted coordinates
    erosion=cv2.erode(mask,kernel=kernel_rect,iterations=1)
    # set mask: zero everywhere exept target zones
    output_img_blue = img.copy()
    output_img_blue[np.where(mask == 0)] = 0
    return mask #,output_img_blue

def green_mask(img):
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #define range of green in hsv
    lower_green = np.array([20, 100, 100])
    upper_green = np.array([100, 255, 255])

    #Treshold the HSV image to get only green colors
    mask=cv2.inRange(img_hsv,lower_green,upper_green)
    #set mask to zero everywhere exept sphero
    output_img_green=img.copy()
    output_img_green[np.where(mask==0)] = 0

    return mask #,output_img_green

def findDot(contours):
    finalCoordinates = []
    for i in range(0, len(contours)):
        x = 0
        y = 0
        l = len(contours[i])
        if l < 5:
            continue
        n = contours[i]
        for j in range(0, l):
            x += n[j][0][0]
            y += n[j][0][1]
        x /= l
        y /= l
        finalCoordinates.append((x, y))

    #print (finalCoordinates)
    #print (len(finalCoordinates))

    return finalCoordinates

def find_min_path(cent,finalC,nmap):
    lengths=[]
    minimum = 1300
    print("dolzina na fc",len(finalC))
    for i in range(0, len(finalC)):
        print(type(nmap), nmap)
        print('centre', type(cent), cent)
        #print(type(finalC[i]), finalC[i].shape, finalC[i])
        path = astar.find_path(nmap, cent, finalC[i])
        lengths[i] = len(path)
        if lengths[i] < minimum:
            final_path = path
            minimum = lengths[i]
            da=finalC[i]

    return final_path,da

def remove_add(img,da,nmap):
    imge = np.zeros([640, 480, 3], dtype=np.uint8)
    imge.fill(0)
    imge = imge[:, :, 1]
    bluemask= blue_mask(img)

    bluemask=bluemask[da[0]-int(35/ 3.55):da[0]+int(35/ 3.55),da[1]-int(35/ 3.69):da[1]+int(35/ 3.69)]
    bluemask=bluemask+imge
    nmap=nmap+bluemask
    return nmap

def sphero_centar(greenmask):
    one, contours, three = cv2.findContours(greenmask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    p=np.array(findDot(contours))
    p=np.average(p,axis=1)
    print(p[0],p[1])
    return (int(p[0]),int(p[1]))
