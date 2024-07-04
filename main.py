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
AVERAGING_STEPS = int(3)
averaging_counter = 0
average = [0, 0, 0, 0]
offset_fingers = 12 # 0 degree offset
mult = 2 # angle multiplier
write_timeout = 0.01
ard_fingers_port = "COM5"
ard_pose_port = "COM11"
cam_port = 0
rps_enabled = False
rps_timer = 0
rps_duration = 0.75
rps_order = 0
rps_rounds_counter = 0
rps_rounds_max = 2

angle_fingers = [0, 0, 0, 0, 0]
offset_fingers = [-4, 4, 4, -6, -15]
multiplier_fingers = [0.8, 0.8, 0.8, 1, 1.3]

angles_pose = [90, 0, 90, 90]
offset_pose = [0, -36, 0, 0]
multiplier_pose = [1, 2.3, 1, 1]

def calculate_angles_fingers(hand):
    angle_fingers[0] = (angle_line_line(equation_line(hand[0], hand[17]), equation_line(hand[17], hand[19])) + offset_fingers[0]) * multiplier_fingers[0]
    angle_fingers[1] = (angle_line_line(equation_line(hand[0], hand[13]), equation_line(hand[13], hand[15])) + offset_fingers[1]) * multiplier_fingers[1]
    angle_fingers[2] = (angle_line_line(equation_line(hand[0], hand[9]), equation_line(hand[9], hand[11])) + offset_fingers[2]) * multiplier_fingers[2]
    angle_fingers[3] = (angle_line_line(equation_line(hand[0], hand[5]), equation_line(hand[5], hand[7])) + offset_fingers[3]) * multiplier_fingers[3]
    angle_fingers[4] = (angle_line_line(equation_line(hand[0], hand[1]), equation_line(hand[2], hand[4])) + offset_fingers[4]) * multiplier_fingers[4]

def calculate_angles_pose(pose):
    angles_pose[1] = (angle_line_line(equation_line(pose[12], pose[14]), equation_line(pose[14], pose[16])) + offset_pose[1]) * multiplier_pose[1]
    angle_shoulder = angle_line_plane(equation_line(pose[12], pose[14]), equation_plane(pose[11], pose[12], pose[24]))
    if(angle_shoulder is not None):
        angles_pose[3] = (angle_shoulder + offset_pose[3]) * multiplier_pose[3]

def angles2serial(angles):
    result = ""
    for i in range(len(angles)-1):
        result = result + f"{int(angles[i])} "
    result = result + f"{int(angles[-1])}"
    return result

ard_fingers = arduino.Arduino(ard_fingers_port, write_timeout=write_timeout, rate=115200)
ard_pose = arduino.Arduino(ard_pose_port, write_timeout=write_timeout, rate=115200)

cap = cv2.VideoCapture(cam_port) # cv2.CAP_MSMF cv2.CAP_DSHOW
#print(f"Backend: {cap.getBackendName()}")
#cap.set(3, 1280)
#cap.set(4, 720)

detector_hands = detectors.DetectorHandsSolution()
detector_pose = detectors.DetectorPoseSolution()
rps = RPS()
mode = 0

start = time.perf_counter()
while True:
    _, image = cap.read()
    #frame_count += 1
    
    #results_hands = detector_hands.process(image, time_per_frame_ms * frame_count)
    results_hands = detector_hands.process(image)
    results_pose = detector_pose.process(image)
    now = perf_counter()
    
    if((now - start) >= DELAY):
        pose = detector_pose.unpack_results(results_pose)
        if(len(pose) > 0):
            calculate_angles_pose(pose)
            average = [sum(x) for x in zip(average, angles_pose)]
            averaging_counter += 1
            if(averaging_counter == AVERAGING_STEPS):
                average = [int(x // AVERAGING_STEPS) for x in average]
                ard_pose.write(angles2serial(average))
                print(f"Pose angles: {average}")
                average = [0, 0, 0, 0]
                averaging_counter = 0
        
        hands = detector_hands.unpack_results(results_hands)
        if(len(hands) > 0):
            hand = hands[0]
            calculate_angles_fingers(hand)
            gesture = rps.detect(angle_fingers)
            if(mode == 0):
                ard_fingers.write(f"{int(angle_fingers[0])} {int(angle_fingers[1])} {int(angle_fingers[2])} {int(angle_fingers[3])} {int(angle_fingers[4])}")
                #print(reply)
                # if(rps_enabled):
                #     if(rps.check_start(gesture)):
                #         mode = 1
                #         rps_timer = perf_counter()
        # if(mode == 1):
        #     if((perf_counter() - rps_timer) >= rps_duration):
        #         print(rps_order)
        #         if(rps_order == 0):
        #             rps_order = 1
        #             print(ard_fingers.query(angles2serial(rps.countdown_one)))
        #         elif(rps_order == 1):
        #             print(ard_fingers.query(angles2serial(rps.countdown_two)))
        #             rps_order = 2
        #         elif(rps_order == 2):
        #             print(ard_fingers.query(angles2serial(rps.countdown_three)))
        #             rps_order = 3
        #         elif(rps_order == 3):
        #             response = rps.generate()
        #             print(ard_fingers.query(angles2serial(response)))
        #             rps_order = 4
        #             rps_duration = 1.25
        #         else:
        #             if(rps_rounds_counter < rps_rounds_max):
        #                 rps_rounds_counter += 1
        #             else:
        #                 mode = 0
        #                 rps_rounds_counter = 0
                    
        #             rps_order = 0
        #             rps_duration = 0.75
        #         rps_timer = perf_counter()
                    
                
        start = now
    
    image = detector_hands.draw_landmarks(image, results_hands)
    image = detector_pose.draw_landmarks(image, results_pose)
    cv2.imshow("MediaPipe", image)
    cv2.waitKey(5)