import mediapipe as mp
import cv2 
from math import cos,degrees
import numpy as np

cap = cv2.VideoCapture("yoga.mp4")
cap.set(3,1280)
cap.set(4,720)
mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.1,min_tracking_confidence=0.1) as pose:
    
    while cap.isOpened():
        success,frame = cap.read()
        if not success:
            break         
        frame = cv2.flip(frame,1)
        h,w,_ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        if results.pose_landmarks is not None:

            for lmk in range(len(results.pose_landmarks.landmark)):
                x = int(results.pose_landmarks.landmark[lmk].x*w)
                y = int(results.pose_landmarks.landmark[lmk].y*h)
                cv2.circle(frame, (x,y),6,(120,108,250),4)

            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                #print(results.pose_landmarks)
                break
        cv2.imshow("img",frame)
cv2.destroyAllWindows()
               




