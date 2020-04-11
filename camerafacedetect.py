import sys
import numpy
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from openvino.inference_engine import IENetwork, IECore
  
face_ir = 'face-detection-retail-0004.xml'

faces_found = False
cur_request_id = 0

detection_threshold = 0.5

box_color = (0, 255, 0)
box_thickness = 1

camera = PiCamera()
rawCapture = PiRGBArray(camera)

####################### 1. Setup Plugin and Network #######################
start_time = time.time()

# Select the myriad plugin and IRs to be used
ie = IECore()

face_net = IENetwork(model = face_ir, weights = face_ir[:-3] + 'bin')

# Get the input and output node names
face_input_blob = next(iter(face_net.inputs))
face_output_blob = next(iter(face_net.outputs))

# Get the input and output shapes from the input/output nodes
face_input_shape = face_net.inputs[face_input_blob].shape
face_output_shape = face_net.outputs[face_output_blob].shape
face_n, face_c, face_h, face_w = face_input_shape
face_x, face_y, face_detections_count, face_detections_size = face_output_shape
    
# Load the network and get the network shape information
face_exec_net = ie.load_network(network = face_net, device_name = "MYRIAD")

end_time = time.time()
print(f'Loaded network in {(end_time - start_time)}')

####################### 2. Image Preprocessing #######################

start_time = time.time()
camera.capture(rawCapture, format="bgr")
end_time = time.time()
print(f'Captured image in {(end_time - start_time)}')
start_time = time.time()

frame = rawCapture.array

image_w = frame.shape[1]
image_h = frame.shape[0]

# Image preprocessing
image_to_classify = cv2.resize(frame, (face_w, face_h))
image_to_classify = numpy.transpose(image_to_classify, (2, 0, 1))
image_to_classify = image_to_classify.reshape((face_n, face_c, face_h, face_w))

end_time = time.time()
print(f'Preprocessed image in {(end_time - start_time)}')
####################### 3. Run the inference #######################
start_time = time.time()
# queue the inference
face_exec_net.start_async(request_id=cur_request_id, inputs={face_input_blob: image_to_classify})

# wait for inference to complete
if face_exec_net.requests[cur_request_id].wait(-1) == 0:
    end_time = time.time()

    print(f'Feed-forward complete in {(end_time - start_time)}')
    
    # get the inference result
    inference_results = face_exec_net.requests[cur_request_id].outputs[face_output_blob]
    for face_num, detection_result in enumerate(inference_results[0][0]):
        
        # Draw only detection_resultects when probability more than specified threshold
        if detection_result[2] > detection_threshold:
            box_left = int(detection_result[3] * image_w)
            box_top = int(detection_result[4] * image_h)
            box_right = int(detection_result[5] * image_w)
            box_bottom = int(detection_result[6] * image_h)
            class_id = int(detection_result[1])
            
            faces_found = True
                        
            cv2.rectangle(frame, (box_left, box_top), (box_right, box_bottom), box_color, box_thickness)
            

cv2.imshow("face detection retail 0004", frame)
print("Press any key to continue.")
while(True):
    rawkey = cv2.waitKey()
    if rawkey != -1:
        break


