
#%% Imports
import sphero  #it allows you to conect with your sphero, you have this library in your RBMS folder
import numpy as np

import astar
#%%
sph = sphero.Sphero('68:86:E7:07:5A:69') # connection with the sphero (you should look for the adress in your bluetooth setings)

#%%
sph.set_rgb(255,0,0) # with this function you can change the colours(RGB) of your sphero
import time

#%%

#nmap=
#path = astar.find_path(nmap, (), (0,0))
path=[(0,36),(36,36),(35,0),(36,1)]
current=(0,0)

for i in range(0,len(path)):

    nextp = path[i]
    vel= np.sqrt((current[1]-nextp[1])**2+(nextp[0]-current[0])**2)
    #dev=float(nextp[1]-current[1])/(nextp[0]-current[0])
    alfa= (np.pi)/2 - (np.arctan2(nextp[1]-current[1],(nextp[0]-current[0])))
    print(alfa)
    alfad=(alfa*180)/np.pi
    print(alfad)
    if int(alfad) <= 0:
        sph.roll(int(vel), 360+int(alfad))
    else:
        sph.roll(int(vel), int(alfad))
    time.sleep(3)
    current=nextp
# sph.roll(20, 0)
# time.sleep(1)
# #sph.roll(20, 0)
# sph.roll(20,90)
# time.sleep(5)


# import timeit
# timeit.timeit(sph.roll(20,0))#with this function (using polar cordinates) you make your sphero move (first integer indicates speed, and the second integer indicates the angle)
# time.sleep(1)

# naogjanje na alfa tg()
# current= (x1, y1)
# next =(x2,y2)
#alfa= pi/2 - np.atan2(float(y2-y1)/(x2-x1))
#alfadeg=(alfa*180)/pi

# sph.roll(vel,alfadeg)
#delay(val)