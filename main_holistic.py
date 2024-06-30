import arduino
import serial
import time
import numpy as np
import cv2
from time import perf_counter
from tracking_holistic import Detector_holistic
from angle_math import *

DELAY = 0.1 # delay between data packets to arduino
offset = 12 # 0 degree offset
mult = 2 # angle multiplier
write_timeout = 0.01

offset = [0, 0, 0, -6, 0]
multiplier = [0, 0, 0, 1.25, 0]

#ard = arduino.Arduino("COM5", write_timeout=write_timeout)

cap = cv2.VideoCapture(0) # cv2.CAP_MSMF cv2.CAP_DSHOW
#print(f"Backend: {cap.getBackendName()}")
cap.set(3, 1280)
cap.set(4, 720)
detector = Detector_holistic()

angle_fingers = [0, 0, 0, 0, 0]
start = time.perf_counter()
while True:
    _, image = cap.read()
    results = detector.process(image)
    # now = time.perf_counter()
    # if((results is not None) & ((now - start) >= DELAY)):
    #     pose, rhand = detector.unpack_results(results) # type: ignore
    #     if(rhand):
    #         angle_fingers[0] = (angle_line_line(equation_line(rhand[0], rhand[17]), equation_line(rhand[17], rhand[19])) + offset[0]) * multiplier[0]
    #         angle_fingers[1] = (angle_line_line(equation_line(rhand[0], rhand[13]), equation_line(rhand[13], rhand[15])) + offset[1]) * multiplier[1]
    #         angle_fingers[2] = (angle_line_line(equation_line(rhand[0], rhand[9]), equation_line(rhand[9], rhand[11])) + offset[2]) * multiplier[2]
    #         angle_fingers[3] = (angle_line_line(equation_line(rhand[0], rhand[5]), equation_line(rhand[5], rhand[7])) + offset[3]) * multiplier[3]
    #         angle_fingers[4] = (angle_line_line(equation_line(rhand[0], rhand[1]), equation_line(rhand[1], rhand[3])) + offset[4]) * multiplier[4]
    #         #ard.write(int(angle_fingers[3]))
    #         print(angle_fingers[3])
    #     start = now
    
    image = detector.draw_landmarks(image, results)
    cv2.imshow("MediaPipe Holistic", image)
    cv2.waitKey(5)