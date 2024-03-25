import cv2
import numpy as np

vid = cv2.VideoCapture('My Video.mp4')

while vid.isOpened():
    ret, frame = vid.read()

    if ret:


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        color = cv2.bilateralFilter(frame, 9, 300, 300)

        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        cv2.imshow("Cartoon", cartoon)

        if cv2.waitKey(25) == 27:
            break
    else:
        break

vid.release()
cv2.destroyAllWindows()
