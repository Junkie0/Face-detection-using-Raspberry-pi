# Face Detection Project

This project demonstrates face detection using OpenCV and Harcascade in Python. Another Face_detection.py can run on raspberry with serbo pan and tilt so I ran it will move the servos if face is detected, If you tried to move face to boundary it moves the servo to keep you face in the frame.
## Usage

1. Run `face_detection.ipynb`.
2. Detects faces in an image and displays rectangles around them.
3. Detects faces in real-time video from the webcam.

## Using Raspberry pi
Install opencv on raspberry pi
1. update and upgrade the raspberry pi using `sudo apt-get update && upgrade`
2. install opencv using `sudo apt install python3-opencv`
**Check the path of the model/haarcascade**
3. By default pwm output is on 17 and 18, you can change the pinout.
4. You may need Male-To-Female jumper wires

## Run on Raspberry pi
1. Connect camera to raspberry pi
2. Assemble the servo motors using pan tilt and put camera
3. Connect appropriate cables to the Raspberry pi headers
3. Run the `face_detection.py` script

## Files

- `face_detection.ipynb`: Python script.
- `haarcascade_frontalface_default.xml`: Haar cascade file.
- `ur pic`: Sample image.
- `face_detection.py` : Python script for raspberry and camera

## Libraries Used

- `numpy`
- `opencv-python`
- `matplotlib`
- `Rpi.gpio`

## Raspberry pi demo video
- [Link](https://drive.google.com/file/d/1OUY3tJQ0oFSmQRjhjBBoDhrkr-qupV0Y/view?usp=drive_link)

## References

- [OpenCV Documentation](https://opencv.org/)
- [Haar Cascade Classifier Documentation](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html)
