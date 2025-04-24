# 🎯 Smart Vision for Visually Impaired

A lightweight real-time object detection and narration system for visually impaired users, using **TensorFlow Lite**, **Raspberry Pi 4**, and **pyttsx3** for speech output.

---

## 🧠 Overview

This project uses a Raspberry Pi and camera module to detect objects in real-time using a TensorFlow Lite model and narrates them aloud. Ideal for visually impaired assistance and smart wearables.

---

## 🛠️ Hardware Requirements

- ✅ Raspberry Pi 4 (4GB or 8GB recommended)
- 📸 Pi Camera Module v2 / USB Camera
- 🎤 Microphone (optional for voice commands)
- 🔊 Speaker / Earphones (for audio output)
- 💾 MicroSD Card (32GB+ recommended)
- 🔌 Power Supply (5V 3A for Pi 4)

---

## 📦 Software Requirements

- Python 3.7+
- TensorFlow Lite
- OpenCV
- pyttsx3 (offline TTS)
- NumPy

---

## 🔧 Installation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-opencv espeak -y
pip3 install tensorflow numpy pyttsx3 opencv-python
