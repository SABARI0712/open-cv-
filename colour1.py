import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# HSV ranges
lower_red1 = np.array([0,120,70])
upper_red1 = np.array([10,255,255])
lower_red2 = np.array([170,120,70])
upper_red2 = np.array([180,255,255])

lower_green = np.array([36,50,70])
upper_green = np.array([89,255,255])

lower_blue = np.array([94,80,2])
upper_blue = np.array([126,255,255])

def detect_and_draw(frame, mask, color_name, box_color):
    detected = False

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 150:  # lowered threshold
            detected = True
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
            cv2.putText(frame, color_name, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, box_color, 2)

    return detected

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = red_mask1 + red_mask2
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    red_detected = detect_and_draw(frame, red_mask, "RED", (0,0,255))
    green_detected = detect_and_draw(frame, green_mask, "GREEN", (0,255,0))
    blue_detected = detect_and_draw(frame, blue_mask, "BLUE", (255,0,0))

    # PRINT RESULTS
    if red_detected:
        print("RED detected")
    if green_detected:
        print("GREEN detected")
    if blue_detected:
        print("BLUE detected")

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
