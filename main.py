import cv2
import pyttsx3
import numpy as np
import tensorflow as tf

# Path to your TFLite model and label file
MODEL_PATH = 'model.tflite'
LABELS_PATH = 'labels.txt'  # Each line: class name

# Load class labels
with open(LABELS_PATH, 'r') as f:
    class_labels = [line.strip() for line in f.readlines()]

# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Adjust speech rate if needed

# Initialize TFLite interpreter
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# OpenCV video capture (0 for USB cam, or use PiCamera with cv2.VideoCapture(0))
cap = cv2.VideoCapture(0)

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def preprocess(frame, input_shape):
    # Resize and normalize image for model input
    img = cv2.resize(frame, (input_shape[1], input_shape[2]))
    img = img.astype(np.float32)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

print("Starting Smart Vision... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # Preprocess frame for model
    input_data = preprocess(frame, input_details[0]['shape'])

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Get output tensors (modify this part based on your model's output)
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]      # Bounding box coordinates
    classes = interpreter.get_tensor(output_details[1]['index'])[0]    # Class index
    scores = interpreter.get_tensor(output_details[2]['index'])[0]     # Confidence scores

    detected_objects = set()
    for i in range(len(scores)):
        if scores[i] > 0.5:  # Confidence threshold
            class_id = int(classes[i])
            label = class_labels[class_id]
            detected_objects.add(label)
            # Draw bounding box
            ymin, xmin, ymax, xmax = boxes[i]
            (h, w) = frame.shape[:2]
            (startX, startY, endX, endY) = (int(xmin * w), int(ymin * h), int(xmax * w), int(ymax * h))
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Narrate detected objects
    if detected_objects:
        speak("I see: " + ", ".join(detected_objects))

    # Show the frame (optional, comment out if running headless)
    cv2.imshow('Smart Vision', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
