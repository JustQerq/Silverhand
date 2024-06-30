import numpy as np
import cv2
import mediapipe as mp
from mediapipe import solutions
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

class Detector_holistic():
  
  def __init__(self, *args, **kwargs):
    self.model = mp_holistic.Holistic(*args, **kwargs)
  
  def draw_landmarks(self, image, results, rhand=True, lhand=True, body=True, face=True):
    image.flags.writeable = True
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    mp_drawing.draw_landmarks(
      image,
      results.face_landmarks,
      mp_holistic.FACEMESH_CONTOURS,
      landmark_drawing_spec=None,
      connection_drawing_spec=mp_drawing_styles
      .get_default_face_mesh_contours_style())
      
    mp_drawing.draw_landmarks(
      image,
      results.pose_landmarks,
      mp_holistic.POSE_CONNECTIONS,
      landmark_drawing_spec=mp_drawing_styles
      .get_default_pose_landmarks_style())
      
    mp_drawing.draw_landmarks(
      image,
      results.right_hand_landmarks,
      solutions.hands.HAND_CONNECTIONS,
      mp_drawing_styles.get_default_hand_landmarks_style(),
      mp_drawing_styles.get_default_hand_connections_style())
    
    mp_drawing.draw_landmarks(
      image,
      results.left_hand_landmarks,
      solutions.hands.HAND_CONNECTIONS,
      mp_drawing_styles.get_default_hand_landmarks_style(),
      mp_drawing_styles.get_default_hand_connections_style())
    
    return image
  
  def process(self, image):
      
    # To improve performance, marking the image as not writeable
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = self.model.process(image)
    
    return results
  
  def unpack_results(self, results, pose_world=True):
    pose = []
    rhand = []
    
    if(pose_world):
      if(results.pose_world_landmarks):
        for landmark in results.pose_world_landmarks.landmark:
          pose.append(np.array([landmark.x, landmark.y, landmark.z]))
    else:
      if(results.pose_landmarks):
        for landmark in results.pose_landmarks.landmark:
          pose.append(np.array([landmark.x, landmark.y, landmark.z]))
      
    if(results.right_hand_landmarks):
      for landmark in results.right_hand_landmarks.landmark:
        rhand.append(np.array([landmark.x, landmark.y, landmark.z]))
    
    return pose, rhand