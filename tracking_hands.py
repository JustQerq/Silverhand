import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green


class Detector_hands():
    # BaseOptions = mp.tasks.BaseOptions
    # HandLandmarker = mp.tasks.vision.HandLandmarker
    # HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    # HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
    # VisionRunningMode = mp.tasks.vision.RunningMode
    model_path = "./hand_landmarker.task"
    
    def get_result(self, result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.detection_results = result
        
    def __init__(self, *args, **kwargs):
        self.options = mp.tasks.vision.HandLandmarkerOptions(
            base_options = mp.tasks.BaseOptions(model_asset_path=self.model_path),
            running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM,
            result_callback = self.get_result,
            *args, **kwargs)
        self.detection_results = mp.tasks.vision.HandLandmarkerResult([],[],[])
        self.model = mp.tasks.vision.HandLandmarker.create_from_options(self.options)
    
    def process(self, image, timestamp):
        mp_img = mp.Image(image_format = mp.ImageFormat.SRGB, data=image)
        self.model.detect_async(mp_img, timestamp)
        return self.detection_results
    
    def draw_landmarks(self, image, detection_results):
        if(len(detection_results.hand_landmarks) == 0): return image
        handedness_list = detection_results.handedness
        hand_landmarks_list = detection_results.hand_landmarks
        annotated_image = np.copy(image)

        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
        annotated_image,
        hand_landmarks_proto,
        solutions.hands.HAND_CONNECTIONS,
        solutions.drawing_styles.get_default_hand_landmarks_style(),
        solutions.drawing_styles.get_default_hand_connections_style())

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        cv2.putText(annotated_image, f"{handedness[0].category_name}",
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

        return annotated_image
    
    def unpack_results(self, results, hand_world=True):
        #handedness = []
        hands = []
        
        if(hand_world):
            if(results.hand_world_landmarks):
                for hand in results.hand_world_landmarks:
                    hand_landmarks = []
                    for landmark in hand:
                        hand_landmarks.append(np.array([landmark.x, landmark.y, landmark.z]))
                    hands.append(hand_landmarks)
        else:
            if(results.hand_landmarks):
                for hand in results.hand_landmarks:
                    hand_landmarks = []
                    for landmark in hand:
                        hand_landmarks.append(np.array([landmark.x, landmark.y, landmark.z]))
                    hands.append(hand_landmarks)
        
        # if(results.handedness):
        #     for hand in results.handedness:
        #         handedness.append(hand.category_name)
        
        return hands