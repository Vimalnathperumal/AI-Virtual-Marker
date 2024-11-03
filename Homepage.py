import cv2
import mediapipe as mp
import numpy as np
import os
import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FPS, 5)
width = 1280
height = 720
cap.set(3, width)
cap.set(4, height)

# Image that will contain the drawing and then passed to the camera image
imgCanvas = np.zeros((height, width, 3), np.uint8)

# Getting all header images in a list
folderPath = 'Header'
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

# Presettings:
header = overlayList[0]
drawColor = (255, 0, 255)
thickness = 20  # Thickness of the painting
tipIds = [4, 8, 12, 16, 20]  # Fingertips indexes
xp, yp = [0, 0]  # Coordinates that will keep track of the last position of the index finger

# Lock/Unlock variables
isLocked = False  # To track the lock state of the screen
lock_time = 0     # Timer to avoid rapid toggling

with mp_hands.Hands(min_detection_confidence=0.85, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break

        # Flip the image horizontally for a selfie-view display, and convert the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        # Convert the image color back to BGR for OpenCV functions
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get hand landmark positions
                points = [(int(lm.x * width), int(lm.y * height)) for lm in hand_landmarks.landmark]

                # Get fingertip positions
                x1, y1 = points[8]  # Index finger
                x2, y2 = points[12]  # Middle finger
                x3, y3 = points[4]  # Thumb
                x4, y4 = points[20]  # Pinky

                # Detect which fingers are up
                fingers = []
                for id in range(5):
                    if id == 0:  # Thumb
                        fingers.append(1 if points[tipIds[id]][0] < points[tipIds[id] - 1][0] else 0)
                    else:  # Other fingers
                        fingers.append(1 if points[tipIds[id]][1] < points[tipIds[id] - 2][1] else 0)

                # Lock screen when index, middle, and ring fingers are up
                if fingers == [0, 1, 1, 1, 0] and (time.time() - lock_time > 1):
                    isLocked = True
                    lock_time = time.time()
                    print("Screen Locked")

                # Unlock screen when index, middle, ring, and pinky fingers are up
                elif fingers == [0, 1, 1, 1, 1] and (time.time() - lock_time > 1):
                    isLocked = False
                    lock_time = time.time()
                    print("Screen Unlocked")

                # Display lock/unlock status on the screen
                lock_status = "Locked" if isLocked else "Unlocked"
                cv2.putText(image, f"Screen {lock_status}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

                # Show message when screen is locked
                if isLocked:
                    cv2.putText(image, "Screen Locked! Use first four fingers to Unlock", (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    continue  # Skip the drawing logic when locked

                ## Drawing Modes and Controls
                # Selection Mode - Two fingers are up
                if fingers[1] and fingers[2] and not any(fingers[i] for i in [0, 3, 4]):
                    xp, yp = [x1, y1]
                    # Selecting the colors and the eraser on the screen
                    if (y1 < 125):
                        if (170 < x1 < 295):
                            header = overlayList[0]
                            drawColor = (255, 0, 255)
                        elif (436 < x1 < 561):
                            header = overlayList[1]
                            drawColor = (0, 255, 255)
                        elif (700 < x1 < 825):
                            header = overlayList[2]
                            drawColor = (0, 255, 0)
                        elif (980 < x1 < 1105):
                            header = overlayList[3]
                            drawColor = (0, 0, 0)

                    cv2.rectangle(image, (x1 - 10, y1 - 15), (x2 + 10, y2 + 23), drawColor, cv2.FILLED)

                ## Standby Mode - Checking when the index and pinky fingers are open and don't draw
                if fingers[1] and fingers[4] and not any(fingers[i] for i in [0, 2, 3]):
                    # Do nothing in this mode
                    pass

                ## Draw Mode - Only the index finger is up and screen is not locked
                if fingers[1] and not any(fingers[i] for i in [0, 2, 3]) and not isLocked:
                    cv2.circle(image, (x1, y1), int(thickness / 2), drawColor, cv2.FILLED)
                    if xp == 0 and yp == 0:
                        xp, yp = [x1, y1]
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, thickness)
                    xp, yp = [x1, y1]

                ## Adjust thickness - Index finger and thumb together and screen is not locked
                if fingers[1] and fingers[0] and not any(fingers[i] for i in [2, 3, 4]) and not isLocked:
                    # Calculate the distance between the thumb and index finger
                    length = math.hypot(x3 - x1, y3 - y1)
                    thickness = int(np.interp(length, [30, 200], [5, 50]))  # Adjust based on distance
                    cv2.putText(image, f"Thickness: {thickness}", (x1 - 50, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                ## Clear the canvas only if unlocked
                if not any(fingers) and not isLocked:  # Prevent clearing if locked
                    imgCanvas = np.zeros((height, width, 3), np.uint8)  # Only execute if unlocked
                    xp, yp = [0, 0]

        # Set the header in the video frame
        image[0:125, 0:width] = header

        # Combine imgCanvas and camera image
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 5, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(image, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        cv2.imshow('MediaPipe Hands', img)
        if cv2.waitKey(3) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
