import cv2,mediapipe as mp,numpy as np, math

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture("arm.mp4")
count = 0
stage = None

def calculateAngle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    randians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(randians*180.0/np.pi)

    if angle>180.0:
        angle = 360-angle
    return  angle

def armVideo(cap,w,h):
    global count,stage

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as Pose:
        while cap.isOpened():
            success,frame = cap.read()
            if not success:
                print('Not success CameraVideo')
                break

            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False 

            frame = cv2.flip(frame,1)
            results = Pose.process(frame)

            frame.flags.writeable = True 
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            try:

                landmarks = results.pose_landmarks.landmark
                Wrist = [int(landmarks[15].x*w),
                        int(landmarks[15].y*h)]
                
                Elbow = [int(landmarks[13].x*w),
                        int(landmarks[13].y*h)]
                
                Shoulder = [int(landmarks[11].x*w),
                            int(landmarks[11].y*h)]
     
                image = np.zeros((h, w, 3), dtype=np.uint8)
                frame = cv2.circle(image, (Wrist[0],Wrist[1]), 1, (102,255,105), 10)
                frame = cv2.circle(image, (Elbow[0],Elbow[1]), 1, (102,255,105), 10)
                frame = cv2.circle(image, (Shoulder[0],Shoulder[1]), 1, (102,255,105), 10)

                angle = calculateAngle(Wrist,Elbow,Shoulder)
                
               
                if angle >= 150:
                    stage = "down"
                    #print('down')
                if angle < 30 and stage == "down":
                    #print("up")
                    stage ="up"
                    count += 1
                    print(str(count),"--------------------------------------")
                    
                    if count == 10:
                        return count

            except:
                print(" No te ves we ")
                pass

            mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2)
                                      ) #draw landmarks 
            return frame
            

def releaseCam():
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #armVideo(cap,1280,720)
    pass
