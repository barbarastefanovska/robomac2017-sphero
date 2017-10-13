import cv2
import masks
from time import sleep
cap = cv2.VideoCapture(1)

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)

    #sleep(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()