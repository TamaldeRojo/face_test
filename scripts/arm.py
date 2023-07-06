import cv2,mediapipe as mp,numpy as np, math

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
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

def armVideo(cap):
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
                Wrist = [landmarks[15].x,landmarks[15].y]
                Elbow = [landmarks[13].x,landmarks[13].y]
                Shoulder = [landmarks[11].x,landmarks[11].y]
     
                angle = calculateAngle(Wrist,Elbow,Shoulder)
                #print(int(angle))
               
                if angle >= 150:
                    stage = "down"
                    #print('down')
                if angle < 30 and stage == "down":
                    #print("up")
                    stage ="up"
                    count += 1
                    print(str(count),"--------------------------------------")

            except:
                print(" No te ves we ")
                pass

            mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2)
                                      ) #draw landmarks



            cv2.imshow("frame", frame) 

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def releaseCam():
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    armVideo(cap)
