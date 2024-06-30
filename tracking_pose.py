import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

# BaseOptions = mp.tasks.BaseOptions
# PoseLandmarker = mp.tasks.vision.PoseLandmarker
# PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
# PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
# VisionRunningMode = mp.tasks.vision.RunningMode

model_path = "./pose_landmarker_full.task"

class Detector_pose():
    def get_result(self, result: mp.tasks.vision.PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.detection_results = result
        
    def __init__(self, *args, **kwargs):
        self.options = mp.tasks.vision.PoseLandmarkerOptions(
            base_options = mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback = self.get_result,
            *args, **kwargs)
        self.detection_results = mp.tasks.vision.PoseLandmarkerResult([],[],[])
        self.model = mp.tasks.vision.PoseLandmarker.create_from_options(self.options)
    
    def process(self, image, timestamp):
        mp_img = mp.Image(image_format = mp.ImageFormat.SRGB, data=image)
        self.model.detect_async(mp_img, timestamp)
        return self.detection_results
    
    def draw_landmarks(self, image, detection_result):
        if(len(detection_result.pose_landmarks) == 0): return image
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(image)

        # Loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
        return annotated_image
    
    def unpack_results(self, results):
        pose = []
        for landmark in results.pose_world_landmarks[0]:
            pose.append(np.array([landmark.x, landmark.y, landmark.z]))
        
        return pose