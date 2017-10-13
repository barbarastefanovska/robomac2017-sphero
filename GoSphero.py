import numpy as np
import cv2
import sphero
import masks
import time

def move(current,path):
    for i in np.linspace(0,len(path),15):

        nextp = path[(int(i),0)]
        vel = np.sqrt(((current[1]-nextp[1])*(1/3.69))**2+((nextp[0]-current[0])*(1/3.55))**2)
        alfa = np.pi/2 - (np.arctan2(nextp[1]-current[1],(nextp[0]-current[0])))
        alfad = (alfa*180)/np.pi

        if int(alfad) <= 0:
            sph.roll(int(vel), 360+int(alfad))
        else:
            sph.roll(int(vel), int(alfad))
        time.sleep(1)
        current=nextp

sph = sphero.Sphero('68:86:E7:07:5A:69') # connection with the sphero (you should look for the adress in your bluetooth setings)
sph.set_rgb(0,255,0) # with this function you can change the colours(RGB) of your sphero. SELECTED: GREEN

cap = cv2.VideoCapture(0)
c = 0
da = (0, 0)

while(cap.isOpened()):
    ret, img = cap.read()
    greenmask, green = masks.green_mask(img)
    spheroc = masks.sphero_centar(greenmask)
    print('Sphero Centar:',spheroc)
    if c == 0:
        bluemask, blue = masks.blue_mask(img)
        one, contours, three = cv2.findContours(bluemask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
        fc = masks.findDot(contours)
        #print(fc)
        print('dolzina',len(fc))
        nmap = masks.red_mask(img)
        print("ok")
        c=1
    else:
        nmap = masks.red_mask(img)
        nmap = masks.remove_add(img, da, nmap)
    # print('nmap TAPL', type(nmap), type(nmap[0]), type(nmap[1]), nmap)
    nmap = np.array(nmap[0])
    print(nmap)

    fp,da=masks.find_min_path(spheroc, fc, nmap)
    fp=fp[::-1]

    current = spheroc
    move(current,fp)
    fc = fc.remove(da)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()