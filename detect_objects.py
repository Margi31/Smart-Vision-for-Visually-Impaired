from ultralytics import YOLO
import cv2

# Load YOLOv8n model
model = YOLO("yolov8n.pt")

# Set webcam feed
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Webcam not available.")
    exit()

# Define known object heights in cm
KNOWN_HEIGHTS = {
    "person": 170,
    "bottle": 25,
    "cup": 10,
    "laptop": 30,
    "cell phone": 15,
    "tv": 50,
    "chair": 100,
    "book": 30,
    "keyboard": 5,
    "mouse": 4,
    "remote": 15,
    "paper": 29.7,
    "backpack": 45,
    "marker": 14
}

# Calibrated focal length
FOCAL_LENGTH = 56.5

# Create full-screen window
cv2.namedWindow("Real-Time Object Detection", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Real-Time Object Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model.predict(source=frame, imgsz=640, conf=0.4, verbose=False)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        box_height = y2 - y1

        # Estimate distance
        if label in KNOWN_HEIGHTS and box_height > 0:
            real_height = KNOWN_HEIGHTS[label]
            distance_cm = (real_height * FOCAL_LENGTH) / box_height
            distance_text = f"{distance_cm:.1f} cm"
        else:
            distance_text = "unknown"

        # Draw bounding box and caption
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        caption = f"{label} ({conf:.2f}) | {distance_text}"
        cv2.putText(frame, caption, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

    # Display result
    cv2.imshow("Real-Time Object Detection", frame)

    # Exit on 'q' or window close
    if cv2.getWindowProperty("Real-Time Object Detection", cv2.WND_PROP_VISIBLE) < 1:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
