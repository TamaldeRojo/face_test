import mediapipe as mp
import cv2 
from math import cos,degrees
import numpy as np
import imutils

cap = cv2.VideoCapture("legs.mp4")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
stage = None
count = 0
def calculateAngle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    randians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(randians*180.0/np.pi)

    if angle>180.0:
        angle = 360-angle
    return  angle

def yoga(cap,w,h):
    global stage,count
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        frame_count = 0
        frames_to_skip = 5
        while cap.isOpened():
            frame_count += 1
            success,frame = cap.read()
            if not success:
                break
            if frame_count % frames_to_skip != 0:
                    continue
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
                
            frame = cv2.flip(frame,1)
            results = pose.process(frame)

            frame.flags.writeable = True 
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            try:
                landmarks = results.pose_landmarks.landmark
                
                Hips = [
                        (int(landmarks[23].x*w),
                         int(landmarks[23].y*h)),
                        
                        (int(landmarks[24].x*w),
                         int(landmarks[24].y*h))
                        ]
                
                knees = [
                        (int(landmarks[26].x*w),
                        int(landmarks[26].y*h)),
                        
                         (int(landmarks[25].x*w),
                         int(landmarks[25].y*h))
                         ]
                
                midHip = [
                    int(((Hips[0][0] + Hips[1][0])/2)),
                    int(((Hips[0][1] + Hips[1][1])/2))
                        ]
                angle = calculateAngle(knees[0],midHip,knees[1])
                print(angle)
                
                if angle >= 60:
                    stage = "up"
                if angle < 20 and stage == "up":
                    stage = "down"
                    count += 1
                    print(str(count)) 
                
                img = np.zeros((h, w, 3), dtype=np.uint8)
                frame = cv2.circle(img, (midHip[0],midHip[1]), 1, (102,255,105), 10)
            except:
                print('no jala')
                
            mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2)
                                      ) 
            frame = imutils.resize(frame, width=320)
            
            return frame, count
            
if __name__ == "__main__":
    yoga(cap,1280,720)
        

               




