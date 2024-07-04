import arduino
import serial
import time
import numpy as np
import cv2
from time import perf_counter
import detectors
from angle_math import *
from RPS import RPS

DELAY = 0.1 # delay between data packets to arduino
offset_fingers = 12 # 0 degree offset
mult = 2 # angle multiplier
write_timeout = 0.01
ard_port = "COM5"
ard_pose_port = "COM11"
cam_port = 1
rps_enabled = True
rps_timer = 0
rps_duration = 0.75
rps_order = 0
rps_rounds_counter = 0
rps_rounds_max = 2

angle_fingers = [0, 0, 0, 0, 0]
offset_fingers = [-4, 4, 4, -6, -15]
multiplier_fingers = [0.8, 0.8, 0.8, 1, 1.3]

def calculate_angles_fingers(hand):
    angle_fingers[0] = (angle_line_line(equation_line(hand[0], hand[17]), equation_line(hand[17], hand[19])) + offset_fingers[0]) * multiplier_fingers[0]
    angle_fingers[1] = (angle_line_line(equation_line(hand[0], hand[13]), equation_line(hand[13], hand[15])) + offset_fingers[1]) * multiplier_fingers[1]
    angle_fingers[2] = (angle_line_line(equation_line(hand[0], hand[9]), equation_line(hand[9], hand[11])) + offset_fingers[2]) * multiplier_fingers[2]
    angle_fingers[3] = (angle_line_line(equation_line(hand[0], hand[5]), equation_line(hand[5], hand[7])) + offset_fingers[3]) * multiplier_fingers[3]
    angle_fingers[4] = (angle_line_line(equation_line(hand[0], hand[1]), equation_line(hand[2], hand[4])) + offset_fingers[4]) * multiplier_fingers[4]

def angles2serial(angles):
    result = ""
    for i in range(len(angles)-1):
        result = result + f"{int(angles[i])} "
    result = result + f"{int(angles[-1])}"
    return result

ard = arduino.Arduino(ard_port, write_timeout=write_timeout, rate=115200)
ard_pose = arduino.Arduino(ard_pose_port, write_timeout=write_timeout, rate=115200)

cap = cv2.VideoCapture(cam_port) # cv2.CAP_MSMF cv2.CAP_DSHOW
#print(f"Backend: {cap.getBackendName()}")
#cap.set(3, 1280)
#cap.set(4, 720)

# FPS = 60
# time_per_frame_ms = int(1000 // FPS)
# frame_count = -1
#detector_hands = detectors.DetectorHandsTask()
detector_hands = detectors.DetectorHandsSolution()
rps = RPS()
mode = 0

ard_pose.write(angles2serial([90, 45, 90, 30]))

start = time.perf_counter()
while True:
    _, image = cap.read()
    #frame_count += 1
    
    #results_hands = detector_hands.process(image, time_per_frame_ms * frame_count)
    results_hands = detector_hands.process(image)
    now = perf_counter()
    
    if((now - start) >= DELAY):
        hands = detector_hands.unpack_results(results_hands)
        if(len(hands) > 0):
            hand = hands[0]
            calculate_angles_fingers(hand)
            gesture = rps.detect(angle_fingers)
            if(mode == 0):
                #ard.write(f"{int(angle_fingers[0])} {int(angle_fingers[1])} {int(angle_fingers[2])} {int(angle_fingers[3])} {int(angle_fingers[4])}")
                print(angles2serial(angle_fingers))
                #print(reply)
                if(rps_enabled):
                    if(rps.check_start(gesture)):
                        mode = 1
                        rps_timer = perf_counter()
        if(mode == 1):
            if((perf_counter() - rps_timer) >= rps_duration):
                print(f"RPS order: {rps_order}")
                if(rps_order == 0):
                    rps_order = 1
                    print(ard.write(angles2serial(rps.countdown_one)))
                elif(rps_order == 1):
                    print(ard.write(angles2serial(rps.countdown_two)))
                    rps_order = 2
                elif(rps_order == 2):
                    print(ard.write(angles2serial(rps.countdown_three)))
                    rps_order = 3
                elif(rps_order == 3):
                    response = rps.generate()
                    print(ard.write(angles2serial(response)))
                    rps_order = 4
                    rps_duration = 1.25
                else:
                    if(rps_rounds_counter < rps_rounds_max):
                        rps_rounds_counter += 1
                    else:
                        mode = 0
                        rps_rounds_counter = 0
                    
                    rps_order = 0
                    rps_duration = 0.75
                rps_timer = perf_counter()
                    
                
        start = now
    
    image = detector_hands.draw_landmarks(image, results_hands)
    cv2.imshow("MediaPipe Hands", image)
    cv2.waitKey(5)