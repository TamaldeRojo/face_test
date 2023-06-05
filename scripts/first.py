import cv2
import mediapipe as mp
import numpy as np

mp_dibujo = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculateAngle(a,b,c):
                a = np.array(a)
                b = np.array(b)
                c = np.array(c)

                radians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
                angle = np.abs(radians*180.0/np.pi)

                if angle >180.0:
                    angle = 360-angle
                return angle

#Video feed
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

with mp_pose.Pose(min_detection_confidence=1,min_tracking_confidence=1) as pose: #mediapipe instance
    while cap.isOpened():
        ret,frame = cap.read()

        #bgr to rgb
        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #bc mediapipe needs rgb
        img.flags.writeable = False 

        #make detection
        results = pose.process(img)

        #rgb to bgr
        img.flags.writeable = True
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
       
        mp_dibujo.draw_landmarks(img, results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                 mp_dibujo.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                 mp_dibujo.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2)
                                 )
        
        try:
            
            landmarks = results.pose_landmarks.landmark
            
            #print('Nariz: ')
            #print(landmarks)
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            

            angle = calculateAngle(shoulder,elbow,wrist)
            print(angle)

            font = cv2.FONT_HERSHEY_SIMPLEX
            
            
            #flipAngle = str(angle)[::-1]
            #print(str(angle)+' '+flipAngle)
            img = cv2.putText(img,str(angle),tuple(np.multiply(elbow,[1280,720]).astype(int)),font,1,(128,248,56),2,cv2.LINE_AA)
            img = cv2.flip(img,1)
            #print(landmarks)
        except:
            print('nothing')
            pass

        #render detections 

        
        cv2.imshow("Mediapipe",img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

