from picamera.array import PiRGBArray
from picamera import PiCamera
from facedetector import FaceDetector
import time
import cv2

box_color = (0, 255, 0)
box_thickness = 1

facedetector = FaceDetector()
camera = PiCamera()
rawCapture = PiRGBArray(camera)

start_time = time.time()
camera.capture(rawCapture, format="bgr")
end_time = time.time()
print(f'Captured image in {(end_time - start_time)}')
start_time = time.time()

frame = rawCapture.array
                     
faces = facedetector.get_faces(frame)
for face in faces:                
    cv2.rectangle(frame, face[0], face[1], box_color, box_thickness)
            
cv2.imshow("face detection", frame)
print("Press any key to continue.")
while(True):
    rawkey = cv2.waitKey()
    if rawkey != -1:
        break

