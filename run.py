from picamera.array import PiRGBArray
from picamera import PiCamera
from facedetector import FaceDetector
from aim import aim
import time

camera = PiCamera()
facedetector = FaceDetector()

while True:   
    start_time = time.time()
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    end_time = time.time()
    print(f'Captured image in {(end_time - start_time)}')
    box_color = (0, 255, 0)
    box_thickness = 1

    frame = rawCapture.array
    faces = facedetector.get_faces(frame)
    
    if len(faces) == 1:
        face = faces[0]
        p1 = face[0]
        p2 = face[1]
        
        image_w = frame.shape[1]
        image_h = frame.shape[0]
        
        w = (p1[0] + p2[0]) / 2 / image_w
        h = (p1[1] + p2[1]) / 2 / image_h
        
        # print(w, ' ', h)
        aim(w, h)