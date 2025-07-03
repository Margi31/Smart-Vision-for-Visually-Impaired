## 🎯 Smart Vision for Visually Impaired
A real-time object detection and narration system built using YOLOv8, TensorFlow Lite, and Raspberry Pi 4. Designed to assist visually impaired individuals by recognizing surroundings and speaking the names of detected objects.

---

## 🧠 Overview
This project leverages the accuracy of YOLOv8 for object detection, exports the model to TensorFlow Lite for efficient edge inference on Raspberry Pi, and narrates detected objects using offline text-to-speech (TTS).

---

## 🛠️ Hardware Requirements
- ✅ Raspberry Pi 4 (4GB or 8GB)
- 📸 Pi Camera Module v2 / USB Camera
- 🔊 Speaker or Earphones
- 💾 MicroSD Card (32GB+)
- 🔌 Power Adapter (5V 3A)

---

## 📦 Software Requirements
- Python 3.8+
- TensorFlow Lite
- ultralytics library for YOLOv8
- pyttsx3 (offline TTS)

---

## 🚀 Installation

```bash
# Update and upgrade your Raspberry Pi
sudo apt update && sudo apt upgrade -y

# Install Python and system dependencies
sudo apt install python3-pip python3-opencv espeak -y

# Install Python libraries
pip install ultralytics
pip install pyttsx3 opencv-python tflite-runtime
