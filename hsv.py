import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Your original HSV ranges
lower_red1 = np.array([0, 120, 70]); upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70]); upper_red2 = np.array([180, 255, 255])
lower_green = np.array([36, 50, 70]); upper_green = np.array([89, 255, 255])
lower_blue = np.array([94, 80, 2]); upper_blue = np.array([126, 255, 255])

blue_mode = False
mouse_pos = (0, 0)

def mouse_callback(event, x, y, flags, param):
    global mouse_pos
    mouse_pos = (x, y)

while True:
    ret, frame = cap.read()
    if not ret: break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width = frame.shape[:2]
    
    # Create all masks (your original logic)
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = red_mask1 + red_mask2
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    display = frame.copy()
    
    if blue_mode:
        # ONLY BLUE visible - others completely black
        display = cv2.bitwise_and(frame, frame, mask=blue_mask)
        
        # Show current HSV bounds
        hsv_text = f"BLUE HSV: H[{lower_blue[0]}-{upper_blue[0]}] S[{lower_blue[1]}-{upper_blue[1]}] V[{lower_blue[2]}-{upper_blue[2]}]"
        cv2.putText(display, hsv_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Show HSV value under mouse cursor (only if on blue area)
        h, s, v = hsv[mouse_pos[1], mouse_pos[0]]
        cursor_text = f"Cursor HSV: [{int(h)}, {int(s)}, {int(v)}]"
        cv2.putText(display, cursor_text, (10, height-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.circle(display, mouse_pos, 5, (0, 255, 0), -1)  # Mouse cursor indicator
        
        cv2.putText(display, "BLUE MODE - Move mouse over blue", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    else:
        # Normal mode - show all colors normally
        cv2.putText(display, "NORMAL - Press 'b' for Blue Only", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Always show blue intensity percentage
    blue_pixels = np.sum(blue_mask > 0)
    blue_percent = blue_pixels / (width * height) * 100
    cv2.putText(display, f"Blue: {blue_percent:.1f}%", (10, height-60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    
    cv2.imshow("Color Detection - 'b'=Blue Only, 'q'=Quit", display)
    cv2.setMouseCallback("Color Detection - 'b'=Blue Only, 'q'=Quit", mouse_callback)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    elif key == ord('b'): 
        blue_mode = not blue_mode

cap.release()
cv2.destroyAllWindows()
