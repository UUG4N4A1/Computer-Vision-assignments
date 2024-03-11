import numpy as np
import cv2 as cv

camera = cv.VideoCapture(0)
target_format = 'avi'
target_fourcc = cv.VideoWriter_fourcc(*'XVID')

fps = camera.get(cv.CAP_PROP_FPS)
wait_msec = int(1 / fps * 1000)

target = None

mode = 'preview'
window_name = 'Video player'

while True:
    if mode == 'preview':
        valid, img = camera.read()
        cv.imshow(window_name, img)
    elif mode == 'record':
        valid, img = camera.read()
        
        if not target:
            target = cv.VideoWriter(f'recording.{target_format}', target_fourcc, fps, (img.shape[1], img.shape[0]))

        center = (50, 100)
        pt = (60, 105)
        cv.circle(img, center, radius=5, color=(0, 0, 255), thickness=-1)
        cv.putText(img, 'Rec', pt, cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
        cv.imshow('Camera', img)

        target.write(img)

    elif mode == 'inverted':
        valid, img = camera.read()
        inverted_img = cv.bitwise_not(img)
        cv.imshow('Inverted', inverted_img)
        
    if not valid:
        break

    key = cv.waitKey(wait_msec)

    if key == 27:  # ESC key: quit program
        break
    elif key == 32:  # Space key: change mode
        if mode == 'preview':
            mode = 'record'
            window_name = 'Camera'
            cv.destroyWindow('Video player')
        elif mode == 'record':
            mode = 'preview'
            window_name = 'Video player'
            cv.destroyWindow('Camera')
            if target:
                target.release()
                target = None
        elif mode == 'inverted':
            mode = 'inverted'
            window_name = 'Inverted'
            cv.destroyWindow('Camera')
            cv.destroyWindow('Video Player')
    elif key == 105 or key == 73:  # ASCII for 'i' and 'I'
        mode = 'inverted'

camera.release()
if target:
    target.release()
cv.destroyAllWindows()
