import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Initialize arrays for different colors
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# Initialize indices for each color
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# Kernel for dilation
kernel = np.ones((5, 5), np.uint8)

# Colors (Blue, Green, Red, Yellow)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Canvas setup (white background)
paintWindow = np.zeros((720, 1280, 3), dtype=np.uint8) + 255
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow('Paint', 1280, 720)  # Resize window for better fit

# Initialize MediaPipe Hands module
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

heightSmall, widthSmall = 240, 426  # Increase webcam feed size
cursor_radius = 3

# Main loop
ret = True
while ret:
    # Read each frame from the webcam
    ret, frame = cap.read()

    # Check if the frame is valid
    if not ret or frame is None:
        print("Failed to capture frame. Exiting...")
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB (MediaPipe expects RGB)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Draw rectangles for the buttons
    cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
    cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), 2)
    cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), 2)
    cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)
    cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), 2)

    # Add text labels for buttons
    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    # Hand landmark prediction
    result = hands.process(framergb)

    # If landmarks are detected, process them
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)
                landmarks.append([lmx, lmy])
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

        # Get fingertip and thumb coordinates
        fore_finger = (landmarks[8][0], landmarks[8][1])
        center = fore_finger
        thumb = (landmarks[4][0], landmarks[4][1])

        # Set up the paint window for drawing
        paintWindow = np.zeros((720, 1280, 3), dtype=np.uint8) + 255  # Increased size
        cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
        cv2.rectangle(paintWindow, (160, 1), (255, 65), (255, 0, 0), 2)
        cv2.rectangle(paintWindow, (275, 1), (370, 65), (0, 255, 0), 2)
        cv2.rectangle(paintWindow, (390, 1), (485, 65), (0, 0, 255), 2)
        cv2.rectangle(paintWindow, (505, 1), (600, 65), (0, 255, 255), 2)
        cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        # Draw the cursor circle for the selected color
        if colorIndex == 0:
            cv2.circle(paintWindow, center, cursor_radius, colors[colorIndex], -1)
        elif colorIndex == 1:
            cv2.circle(paintWindow, center, cursor_radius, colors[colorIndex], -1)
        elif colorIndex == 2:
            cv2.circle(paintWindow, center, cursor_radius, colors[colorIndex], -1)
        elif colorIndex == 3:
            cv2.circle(paintWindow, center, cursor_radius, colors[colorIndex], -1)

        # Update the points if the thumb is close to the center
        if (thumb[1] - center[1] < 30):
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1
        elif center[1] <= 65:
            if 40 <= center[0] <= 140:  # Clear button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0
                paintWindow[67:, :, :] = 255
            elif 160 <= center[0] <= 255:
                colorIndex = 0  # Blue
            elif 275 <= center[0] <= 370:
                colorIndex = 1  # Green
            elif 390 <= center[0] <= 485:
                colorIndex = 2  # Red
            elif 505 <= center[0] <= 600:
                colorIndex = 3  # Yellow
        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

    # Draw the lines on the canvas for each color
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    # Resize webcam feed and display it in the bottom-right corner
    imgSmall = cv2.resize(frame, (widthSmall, heightSmall))
    h, w, _ = paintWindow.shape
    paintWindow[h - heightSmall:h, w - widthSmall:w] = imgSmall

    if cv2.getWindowProperty("Paint", cv2.WND_PROP_VISIBLE) < 1:
        break

    # Show the frame and canvas
    cv2.imshow("Paint", paintWindow)

    # Check for key press (exit on 'q')
    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()