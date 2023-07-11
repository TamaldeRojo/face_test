from math import acos,degrees
import cv2
import mediapipe as mp 
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
up = False
down = False
count = 0

cap=cv2.VideoCapture("squats.mp4")

def calculateAngle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    randians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(randians*180.0/np.pi)

    if angle>180.0:
        angle = 360-angle
    return  angle

def videoSquats(cap):
        global count
        global down
        global up
        with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
            
            while cap.isOpened():
                
                success, frame = cap.read()
                if not success:
                    print('Not success CameraVideo')
                    break
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame.flags.writeable = False
                
                frame = cv2.flip(frame,1)
                results = pose.process(frame)

                frame.flags.writeable = True 
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark
                    hip = [int(landmarks[23].x*1280),
                           int(landmarks[23].y*720)]
                    
                    knee = [int(landmarks[25].x*1280),
                           int(landmarks[25].y*720)]
                    
                    ankle = [int(landmarks[27].x*1280),
                           int(landmarks[27].y*720)]

                    angle = calculateAngle(hip,knee,ankle)

                    image = np.zeros((720, 1280, 3), dtype=np.uint8)
                    frame = cv2.circle(image, (hip[0],hip[1]), 1, (102,255,105), 10)
                    frame = cv2.circle(image, (knee[0],knee[1]), 1, (102,255,105), 10)
                    frame = cv2.circle(image, (ankle[0],ankle[1]), 1, (102,255,105), 10)
                    #print(int(angle))
                    if angle >= 150:
                            up = True #parado
                    if up == True and down == False and angle <= 149 and angle>=51:
                            down = True #flexionado
                        
                    if up == True and down == True and angle >= 50:
                        count += 1
                        up = False
                        down = False
                        print(count)
                        
                    if count == 4:
                        return count
                    
                    
                    

                except:
                    print("no jala we")
                
                mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2)
                                      ) #draw landmarks

                cv2.imshow("frame", frame) 
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
def release_camera():
        cap.release()
        cv2.destroyAllWindows()      

if __name__ == "__main__":
    videoSquats(cap)
    release_camera()