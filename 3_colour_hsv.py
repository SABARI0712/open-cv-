import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Your original HSV ranges
lower_red1 = np.array([0, 120, 70]); upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70]); upper_red2 = np.array([180, 255, 255])
lower_green = np.array([36, 50, 70]); upper_green = np.array([89, 255, 255])
lower_blue = np.array([94, 80, 2]); upper_blue = np.array([126, 255, 255])

mode = None  # 'red', 'green', 'blue', or None (normal)
mouse_pos = (0, 0)

def mouse_callback(event, x, y, flags, param):
    global mouse_pos
    mouse_pos = (x, y)

while True:
    ret, frame = cap.read()
    if not ret: break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width = frame.shape[:2]
    
    # All masks (your original logic)
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = red_mask1 + red_mask2
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    display = frame.copy()
    
    if mode == 'red':
        display = cv2.bitwise_and(frame, frame, mask=red_mask)
        bounds_text = f"RED HSV: H[{lower_red1[0]}-{upper_red1[0]},{lower_red2[0]}-{upper_red2[0]}] S[{lower_red1[1]}-{lower_red1[1]}] V[{lower_red1[2]}-{255}]"
        cv2.putText(display, bounds_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        color_pct = np.sum(red_mask > 0) / (width * height) * 100
        cv2.putText(display, f"Red: {color_pct:.1f}%", (10, height-60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
    elif mode == 'green':
        display = cv2.bitwise_and(frame, frame, mask=green_mask)
        bounds_text = f"GREEN HSV: H[{lower_green[0]}-{upper_green[0]}] S[{lower_green[1]}-{upper_green[1]}] V[{lower_green[2]}-{255}]"
        cv2.putText(display, bounds_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        color_pct = np.sum(green_mask > 0) / (width * height) * 100
        cv2.putText(display, f"Green: {color_pct:.1f}%", (10, height-60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
    elif mode == 'blue':
        display = cv2.bitwise_and(frame, frame, mask=blue_mask)
        bounds_text = f"BLUE HSV: H[{lower_blue[0]}-{upper_blue[0]}] S[{lower_blue[1]}-{upper_blue[1]}] V[{lower_blue[2]}-{upper_blue[2]}]"
        cv2.putText(display, bounds_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        color_pct = np.sum(blue_mask > 0) / (width * height) * 100
        cv2.putText(display, f"Blue: {color_pct:.1f}%", (10, height-60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
    else:  # Normal mode
        cv2.putText(display, "NORMAL: r=red, g=green, b=blue, q=quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Mouse HSV (all modes)
    if mode:
        h, s, v = hsv[mouse_pos[1], mouse_pos[0]]
        cursor_text = f"Cursor HSV: H{int(h)} S{int(s)} V{int(v)}"
        cv2.putText(display, cursor_text, (10, height-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.circle(display, mouse_pos, 5, (0, 255, 0), -1)
    
    cv2.imshow("Multi-Color Detector", display)
    cv2.setMouseCallback("Multi-Color Detector", mouse_callback)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    elif key == ord('r'): mode = 'red' if mode != 'red' else None
    elif key == ord('g'): mode = 'green' if mode != 'green' else None
    elif key == ord('b'): mode = 'blue' if mode != 'blue' else None

cap.release()
cv2.destroyAllWindows()
