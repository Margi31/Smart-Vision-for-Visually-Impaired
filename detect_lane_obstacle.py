from ultralytics import YOLO
import cv2
import time
import torch
import pyttsx3  # Voice alerts

# Load YOLO Nano model
model = YOLO("yolov8n.pt")  # Nano model for speed
if torch.cuda.is_available():
    model.to("cuda")
    print("🔋 Using GPU")
else:
    print("⚙ Using CPU")

# Constants
FOCAL_LENGTH = 615  # Adjusted based on your setup
CLOSE_THRESHOLD_CM = 100
KNOWN_HEIGHTS = {"person": 165, "chair": 100, "bottle": 25}  # Add more as needed

# TTS setup (female voice)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 160)

def estimate_distance(box_height, label):
    if label in KNOWN_HEIGHTS:
        real_height = KNOWN_HEIGHTS[label]
        distance_cm = (real_height * FOCAL_LENGTH) / box_height
        return round(distance_cm, 1)
    return None

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Couldn't open {video_path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize to 960x540 (16:9) for better speed and view
        frame = cv2.resize(frame, (960, 540))

        results = model(frame, verbose=False)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                label = model.names[cls_id].lower()

                box_height = y2 - y1
                distance = estimate_distance(box_height, label)

                color = (0, 255, 0)
                alert_text = ""

                if distance is not None and distance < CLOSE_THRESHOLD_CM:
                    color = (0, 0, 255)
                    alert_text = f"🚨 {label} too close!"

                    # Speak only once per object
                    engine.say(f"Warning! {label} is close.")
                    engine.runAndWait()

                    cv2.putText(frame, alert_text, (x1, y1 - 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                # Label + distance
                text = f"{label} {conf:.2f}"
                if distance is not None:
                    text += f" | {distance:.1f} cm"

                cv2.putText(frame, text, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Display the video
        cv2.namedWindow("Smart Vision Detection", cv2.WINDOW_NORMAL)
        cv2.imshow("Smart Vision Detection", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run
process_video("1Video.mp4")
