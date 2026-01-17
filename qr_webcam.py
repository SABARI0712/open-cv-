import cv2

def main():
    # Open webcam
    cap = cv2.VideoCapture(0)

    # QR Code detector
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect and decode QR
        data, points, _ = detector.detectAndDecode(frame)

        if data:
            print("QR Detected:", data)

            if points is not None:
                points = points[0]  # Get corner points (4 points)

                # Draw bounding box
                for i in range(len(points)):
                    pt1 = (int(points[i][0]), int(points[i][1]))
                    pt2 = (int(points[(i + 1) % len(points)][0]), int(points[(i + 1) % len(points)][1]))
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

                # Draw text near QR
                x = int(points[0][0])
                y = int(points[0][1])
                cv2.putText(frame, data, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Show webcam window
        cv2.imshow("QR Scanner", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

