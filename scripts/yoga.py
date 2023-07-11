import mediapipe as mp
import cv2 
from math import cos,degrees
import numpy as np

cap = cv2.VideoCapture("yoga.mp4")
cap.set(3,1280)
cap.set(4,720)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def yoga(cap):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success,frame = cap.read()
            if not success:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
                
            frame = cv2.flip(frame,1)
            results = pose.process(frame)

            frame.flags.writeable = True 
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            try:
                frame = np.zeros((720, 1280, 3), dtype=np.uint8)
            except:
                print('no jala')
                
            mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2)
                                      ) 
            
            cv2.imshow("img",frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            
if __name__ == "__main__":
    yoga(cap)
        

               




