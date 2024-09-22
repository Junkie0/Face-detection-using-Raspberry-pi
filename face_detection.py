#!/usr/bin/env python
import cv2, sys, time, os
import RPi.GPIO as GPIO  # Import RPi.GPIO for controlling the servos

# Load the BCM V4l2 driver for /dev/video0
os.system('sudo modprobe bcm2835-v4l2')
# Set the framerate
os.system('v4l2-ctl -p 40')

# Frame Size
FRAME_W = 320
FRAME_H = 200

# Default Pan/Tilt for the camera in degrees
cam_pan = 7.5  # Neutral position for the servo (90 degrees corresponds to a 7.5% duty cycle)
cam_tilt = 7.5

# Set up the Cascade Classifier for face tracking
cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

# Start and set up the video capture with selected frame size
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)
time.sleep(2)

# Set up the GPIO pins for the servos
PAN_PIN = 17   # GPIO pin for pan servo
TILT_PIN = 18  # GPIO pin for tilt servo

# Set up the GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PAN_PIN, GPIO.OUT)
GPIO.setup(TILT_PIN, GPIO.OUT)

# Set up PWM for the servos (50Hz frequency is typical for servos)
pan_pwm = GPIO.PWM(PAN_PIN, 50)
tilt_pwm = GPIO.PWM(TILT_PIN, 50)

# Start PWM with neutral position
pan_pwm.start(cam_pan)  # 7.5% duty cycle corresponds to 90 degrees (neutral position)
tilt_pwm.start(cam_tilt)

# Function to update the servo positions
def update_servos(pan_pos, tilt_pos):
    pan_pwm.ChangeDutyCycle(pan_pos)
    tilt_pwm.ChangeDutyCycle(tilt_pos)

# Infinite loop to capture and process frames
while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)
    
    if not ret:
        print("Error getting image")
        continue

    # Convert to greyscale for easier and faster face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Detect faces in the frame
    faces = faceCascade.detectMultiScale(frame, 1.1, 3, 0, (10, 10))

    for (x, y, w, h) in faces:
        # Draw a green rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

        # Get the center of the face
        face_center_x = x + (w // 2)
        face_center_y = y + (h // 2)

        # Correct relative to the center of the image
        turn_x = float(face_center_x - (FRAME_W / 2))
        turn_y = float(face_center_y - (FRAME_H / 2))

        # Convert to percentage offset
        turn_x /= float(FRAME_W / 2)
        turn_y /= float(FRAME_H / 2)

        # Scale offset to duty cycle adjustments (7.5% corresponds to 90 degrees)
        turn_x *= 2.5  # Adjust sensitivity as needed
        turn_y *= 2.5

        cam_pan -= turn_x
        cam_tilt += turn_y

        # Clamp Pan/Tilt to valid duty cycle ranges (2.5 to 12.5% duty cycle for 0 to 180 degrees)
        cam_pan = max(2.5, min(12.5, cam_pan))
        cam_tilt = max(2.5, min(12.5, cam_tilt))

        # Update the servos
        update_servos(cam_pan, cam_tilt)

        break
    
    # Display the video with rectangles overlayed
    frame = cv2.resize(frame, (540, 300))
    frame = cv2.flip(frame, 1)
    cv2.imshow('Video', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
pan_pwm.stop()  # Stop PWM for pan
tilt_pwm.stop()  # Stop PWM for tilt
GPIO.cleanup()  # Clean up GPIO setting
