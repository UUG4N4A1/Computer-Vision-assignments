import cv2
import numpy as np
import time
import handTrackingModule as htm
import math

black = (50, 50, 50)
white = (225, 225, 225)
blue = 	(220,20,60)
green = (34,139,34)
light_blue = 	(255, 215, 0)

zones = {}
forX = {}
forO = {}

horizontal_start = 700
horizontal_end = 1150
vertical_start = 200
vertical_end = 650
step = 150

turn = 0  
board = {i: [] for i in range(1, 10)}

# Initialize necessary dictionaries that later used on drawing shapes and finding zones.
def initialization():
    counter = 1

    for j in range(3):  
        for i in range(3):  
            x_start = horizontal_start + i * step
            x_end = x_start + step
            y_start = vertical_start + j * step
            y_end = y_start + step
            zones[counter] = {'x_range': (x_start, x_end), 'y_range': (y_start, y_end)}
            counter += 1

    for key in range(1, 10):
        forX[key] = set()
    counter = 1
    for j in range(3):
        for i in range(3):
            x_start = horizontal_start + i * step
            x_end = x_start + step
            y_start = vertical_start + j * step
            y_end = y_start + step
            forX[counter] = {(x_start, y_start), (x_end, y_end), (x_start, y_end), (x_end, y_start)}
            counter += 1

    for key in range(1, 10):
        forO[key] = set()
    counter = 1
    for j in range(3):
        for i in range(3):
            x_center = horizontal_start + step // 2 + i * step
            y_center = vertical_start + step // 2 + j * step
            forO[counter] = (x_center, y_center)
            counter += 1
# find zone [1-9] with given value x,y
def find_zone(x, y):
    for zone, ranges in zones.items():
        x_range = ranges['x_range']
        y_range = ranges['y_range']
        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            return zone
    return None
# Drawing field
def draw_field(img):
    
    pt1 = (horizontal_start, vertical_start)
    pt2 = (horizontal_end, vertical_end)
    cv2.rectangle(img, pt1, pt2, white, cv2.FILLED)
    cv2.rectangle(img, pt1, pt2, black, 3)
    cv2.line(img, (pt1[0] + step, pt1[1]), (pt1[0] + step, pt2[1]), black, 3)
    cv2.line(img, (pt1[0] + 2 * step, pt1[1]), (pt1[0] + 2 * step, pt2[1]), black, 3)
    cv2.line(img, (pt1[0], pt1[1] + step), (pt2[0], pt1[1] + step), black, 3)
    cv2.line(img, (pt1[0], pt1[1] + 2 * step), (pt2[0], pt1[1] + 2 * step), black, 3)
    cv2.putText(img,f"Player {'1' if turn == 0 else '2'} turn", (710,190), cv2.FONT_HERSHEY_DUPLEX,2, light_blue, 1)

# Find zone and draw x and Y and store value on board dic
def drawXO(img, pX, pY):
    global turn
    pointX = int(np.interp(pX, [0, 1920], [0, 1280]))
    pointY = int(np.interp(pY, [0, 1080], [0, 720]))
    # check if it is on field or not
    if horizontal_start < pointX < horizontal_end and vertical_start < pointY < vertical_end:
        zone = find_zone(pointX, pointY)
        if zone and turn == 0 and len(board[zone]) == 0:
            print(f"Drawing 'O' at zone {zone} coordinates: {forO[zone]}")
            cv2.circle(img, forO[zone], 25, black, 3)
            turn = 1
            board[zone].append(0)
        elif zone and turn == 1 and len(board[zone]) == 0:
            forX_list = list(forX[zone])
            print(f"Drawing 'X' at zone {zone} coordinates: {forX_list}")
            cv2.line(img, tuple(forX_list[0]), tuple(forX_list[1]), black, 3)
            turn = 0
            board[zone].append(1)

# game logic to determine winner
def game_logic():
    win_conditions = [
        # check diagonally, horizontally, and vertically
        [1, 2, 3], [4, 5, 6], [7, 8, 9], 
        [1, 4, 7], [2, 5, 8], [3, 6, 9], 
        [1, 5, 9], [3, 5, 7]
    ]
    for condition in win_conditions:
        values = [board[pos][0] if board[pos] else -1 for pos in condition]
        if values == [0, 0, 0]:
            return 0 
        elif values == [1, 1, 1]:
            return 1 
    return -1 

def main():
    initialization()
    
    pTime = 0
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = htm.handDetector(detectionCon=0.8, maxHands=1)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        draw_field(img)
        if len(lmList) != 0:
            x1, y1 = lmList[8][1], lmList[8][2]
            x2, y2 = lmList[12][1], lmList[12][2]
            x3, y3 = abs(x1 - x2), abs(y2 - y1)
            center = (x1 + x2 // 2, y1 + y2 // 2)
            center2 = ((x1 + x2) // 2, (y1 + y2) // 2)

            length = math.hypot(x3, y3)
            # cv2.line(img, (x1, y1), (x2, y2), black, 3)
            cv2.circle(img, center2, 25, green, -1)
            if length < 50: 
                cv2.circle(img, center2, 25, blue, -1)
                drawXO(img, center[0], center[1])

        
        result = game_logic()
        if result != -1:
            cv2.putText(img,f"Player {'1' if result == 0 else '2'} wins!", (200,100), cv2.FONT_HERSHEY_DUPLEX, 3, light_blue, 3)
            # print(f"Player {'O' if result == 0 else 'X'} wins!")
            # break

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)

        cv2.imshow("Image", img) 
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

if __name__ == "__main__":
    main()
