import arduino
from angle_math import *

gestures_pose = {}
gestures_fingers = {}

# pose: wrist (keep at 90), elbow (0 to 95), 
# arm rotation (90 to 0 = clockwise, 90 to 180 = counterclockwise), 
# shoulder (0 to 90)

# fingers: pinky to thumb = 1 to 5 (0 to 130 angle)

gestures_pose['neutral'] = [90, 0, 90, 0]
gestures_fingers['neutral'] = [0, 0, 0, 0, 0]

gestures_pose['thumbs up'] = [90, 80, 175, 35]
gestures_fingers['thumbs up'] = [130, 130, 130, 130, 0]

gestures_pose['handshake'] = [90, 40, 110, 20]
gestures_fingers['handshake'] = [30, 30, 30, 30, 30]
gestures_pose['rock and roll'] = [90, 95, 175, 35]
gestures_fingers['rock and roll'] = [0, 130, 130, 0, 0]

def angles2serial(angles):
    result = ""
    for i in range(len(angles)-1):
        result = result + f"{int(angles[i])} "
    result = result + f"{int(angles[-1])}"
    return result

write_timeout = 0.01
ard_fingers_port = "COM5"
ard_pose_port = "COM11"

ard_fingers = arduino.Arduino(ard_fingers_port, write_timeout=write_timeout, rate=115200)
ard_pose = arduino.Arduino(ard_pose_port, write_timeout=write_timeout, rate=115200)

while True:
    gesture = input('Gesture: ')
    try:
        ard_pose.write(angles2serial(gestures_pose[gesture]))
        ard_fingers.write(angles2serial(gestures_fingers[gesture]))
    except:
        print("Unrecognised gesture")
    