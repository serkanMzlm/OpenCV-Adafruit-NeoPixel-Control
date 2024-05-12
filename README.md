# Adafruit NeoPixel control with OpenCV

Using Python with OpenCV, the project allows users to select regions of interest (ROI) on images displayed on the screen (R-G-B) and send information about the desired intensity of red, green, and blue to an Arduino board. The Arduino receives this data and adjusts the Adafruit NeoPixel lights accordingly.

**Note:** To prevent sudden color bursts from the Arduino side, linear Kalman filtering has been incorporated into the code.

### Used Python Modules:
- opencv-python
- cvzone
- HandDetector
- pyserial
- mediapipe

[test.webm](https://github.com/serkanMzlm/OpenCV-Adafruit-NeoPixel-Control/assets/74418302/920a2d29-a7f0-4368-b6fe-7269e8ea4b9a)
