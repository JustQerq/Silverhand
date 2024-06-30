import random
from time import time


class RPS():
    waiting_period = 2
    
    closed_finger = 130
    start_sequence = [1, 2, 3]
    rock = [False, False, False, False, False]
    rock_angles = [closed_finger, closed_finger, closed_finger, closed_finger, closed_finger]
    paper = [True, True, True, True, True]
    paper_angles = [0, 0, 0, 0, 0]
    scissors = [False, False, True, True, False]
    scissors_angles = [closed_finger, closed_finger, 0, 0, closed_finger]
    countdown_one = [closed_finger, closed_finger, closed_finger, 0, closed_finger]
    countdown_two = [closed_finger, closed_finger, 0, 0, closed_finger]
    countdown_three = [closed_finger, 0, 0, 0, closed_finger]
    
    def __init__(self) -> None:
        self.gestures = []
        self.last_check = time()
    
    def angles_to_gesture(self, angles):
        gesture = [False, False, False, False, False]
        if(angles[0] < 50): gesture[0] = True
        if(angles[1] < 50): gesture[1] = True
        if(angles[2] < 50): gesture[2] = True
        if(angles[3] < 50): gesture[3] = True
        if(angles[4] < 30): gesture[4] = True
        return gesture

    def detect(self, angles):
        gesture = self.angles_to_gesture(angles)
        if(gesture == self.rock): return 1
        if(gesture == self.paper): return 2
        if(gesture == self.scissors): return 3
        return 0

    def check_start(self, gesture):
        if((gesture == 0)) : return False
        
        now = time()
        if(now - self.last_check > self.waiting_period):
            self.gestures = []
        elif(len(self.gestures) > 0): 
            if(gesture == self.gestures[-1]):
                return False
        
        if(len(self.gestures) == 3):
            self.gestures = self.gestures[1:]
        
        
        self.last_check = time()
        self.gestures.append(gesture)
        if(self.gestures == self.start_sequence):
            self.gestures = []
            return True
        return False
    
    def generate(self):
        possible_gestures = [self.rock_angles, self.paper_angles, self.scissors_angles]
        gesture_id = random.randint(0, 2)
        return possible_gestures[gesture_id]
        