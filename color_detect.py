import cv2
import numpy as np

# Open the webcam
cap = cv2.VideoCapture(0)

# Define HSV ranges for each color
# You can adjust these later if needed

# RED (two ranges because red wraps around HSV)
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# GREEN
lower_green = np.array([36, 50, 70])
upper_green = np.array([89, 255, 255])

# BLUE
lower_blue = np.array([94, 80, 2])
upper_blue = np.array([126, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create color masks
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = red_mask1 + red_mask2

    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply the mask on image
    red_result = cv2.bitwise_and(frame, frame, mask=red_mask)
    green_result = cv2.bitwise_and(frame, frame, mask=green_mask)
    blue_result = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # Show all
    cv2.imshow("Original", frame)
    cv2.imshow("Red Detection", red_result)
    cv2.imshow("Green Detection", green_result)
    cv2.imshow("Blue Detection", blue_result)

    # Press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

