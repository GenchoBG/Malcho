import sys
import numpy
import cv2
import time
from openvino.inference_engine import IENetwork, IECore

face_ir = 'face-detection-retail-0004.xml'

class FaceDetector():
    def __init__(self, threshold = 0.5):
####################### Setup Plugin and Network #######################
        start_time = time.time()
        
        self.cur_request_id = 0
        self.detection_threshold = threshold

        # Select the myriad plugin and IRs to be used
        ie = IECore()
        face_net = IENetwork(model = face_ir, weights = face_ir[:-3] + 'bin')

        # Get the input and output node names
        self.face_input_blob = next(iter(face_net.inputs))
        self.face_output_blob = next(iter(face_net.outputs))

        # Get the input and output shapes from the input/output nodes
        face_input_shape = face_net.inputs[self.face_input_blob].shape
        face_output_shape = face_net.outputs[self.face_output_blob].shape
        self.face_n, self.face_c, self.face_h, self.face_w = face_input_shape
        face_x, face_y, face_detections_count, face_detections_size = face_output_shape
            
        # Load the network and get the network shape information
        self.face_exec_net = ie.load_network(network = face_net, device_name = "MYRIAD")

        end_time = time.time()
        print(f'Loaded network in {(end_time - start_time)}')


    def get_faces(self, frame):
        faces = []
        
        start_time = time.time()
        image_w = frame.shape[1]
        image_h = frame.shape[0]

        # Image preprocessing
        image_to_classify = cv2.resize(frame, (self.face_w, self.face_h))
        image_to_classify = numpy.transpose(image_to_classify, (2, 0, 1))
        image_to_classify = image_to_classify.reshape((self.face_n, self.face_c, self.face_h, self.face_w))

        end_time = time.time()
        print(f'Preprocessed image in {(end_time - start_time)}')        
        start_time = time.time()
        # queue the inference
        self.face_exec_net.start_async(request_id=self.cur_request_id, inputs={self.face_input_blob: image_to_classify})

        # wait for inference to complete
        if self.face_exec_net.requests[self.cur_request_id].wait(-1) == 0:
            end_time = time.time()

            print(f'Feed-forward complete in {(end_time - start_time)}')
            
            # get the inference result
            inference_results = self.face_exec_net.requests[self.cur_request_id].outputs[self.face_output_blob]
            for face_num, detection_result in enumerate(inference_results[0][0]):
                if detection_result[2] > self.detection_threshold:
                    box_left = int(detection_result[3] * image_w)
                    box_top = int(detection_result[4] * image_h)
                    box_right = int(detection_result[5] * image_w)
                    box_bottom = int(detection_result[6] * image_h)
                    class_id = int(detection_result[1])
                                
                    faces.append(((box_left, box_top), (box_right, box_bottom)))
                    
        return faces

