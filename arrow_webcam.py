import cv2
import numpy as np

def get_direction(cnt):
    # Get contour moments
    M = cv2.moments(cnt)
    if M["m00"] == 0:
        return None

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # Approx polygon to get corners
    approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)

    # Find tip of arrow (point with smallest distance from centroid)
    min_dist = 999999
    tip = None
    for p in approx:
        px, py = p[0]
        dist = (px - cx)**2 + (py - cy)**2
        if dist < min_dist:
            min_dist = dist
            tip = (px, py)

    # Determine direction by comparing tip position with centroid
    if tip:
        tx, ty = tip
        if abs(tx - cx) < 20:   # Almost vertically aligned
            if ty < cy:
                return "UP"
            else:
                return "DOWN"
        else:
            if tx < cx:
                return "LEFT"
            else:
                return "RIGHT"

    return None


def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        _, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            cnt = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(cnt)

            if area > 1500:
                direction = get_direction(cnt)
                x, y, w, h = cv2.boundingRect(cnt)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)

                if direction:
                    cv2.putText(frame, direction, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    print("Detected:", direction)

        cv2.imshow("Arrow Detection", frame)
        cv2.imshow("Threshold", thresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

