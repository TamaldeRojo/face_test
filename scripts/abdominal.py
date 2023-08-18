import cv2,mediapipe as mp, numpy as np, math , imutils

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture("situps.mp4")

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

def abdominal(cap,w,h):
    global count,stage
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as Pose:
        frame_count = 0
        frames_to_skip = 5
        while cap.isOpened():
            
            frame_count += 1
            success,frame = cap.read()
            if not success:
                print("aaaa")
                break
            if frame_count % frames_to_skip != 0:
                    continue
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            
            #frame = cv2.flip(frame,1)
            results = Pose.process(frame)
            
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
           
            try:
                
                #Necesito saber:
                #Que tan cerca esta la nariz de los wrists
                #Que tan cerca esta la nariz de las rodillas
                #El angulo de Rodillas - Cadera - Nariz
                #Que tan cerca estan los pies de las pompis
                               
                landmarks = results.pose_landmarks.landmark
                
                Nose = [int(landmarks[0].x *w),int(landmarks[0].y *h)]
                
                Wrists = [[landmarks[15].x,landmarks[15].y],
                          [landmarks[16].x,landmarks[16].y]]
                
                Hips = [[landmarks[23].x,landmarks[23].y],
                        [landmarks[24].x,landmarks[24].y]]
                
                Heels = [[landmarks[27].x,landmarks[27].y],
                         [landmarks[28].x,landmarks[28].y]] 
                
                knees = [[landmarks[26].x,landmarks[26].y],
                         [landmarks[25].x],landmarks[25].y]
                
                #math 
                midHip = [
                    int(((landmarks[23].x + landmarks[24].x)/2) * w),
                    int(((landmarks[23].y + landmarks[24].y)/2) * h )
                        ]
                #print(midHip)
                
                midKnees = [
                    int(((landmarks[26].x + landmarks[25].x)/2) * w),
                    int(((landmarks[26].y + landmarks[25].y)/2) * h )
                        ]
                
                
                image = np.zeros((h, w, 3), dtype=np.uint8)
                frame = cv2.circle(image, (midHip[0],midHip[1]), 1, (102,255,105), 10)
                frame = cv2.circle(image, (midKnees[0],midKnees[1]), 1, (102,255,105), 10)
                frame = cv2.circle(image, (Nose[0],Nose[1]), 1, (102,255,105), 10)
                
                angle = calculateAngle(Nose,midHip,midKnees)
                #print(str(int(angle)),'<------->','acostado') if angle >= 120 else print(str(int(angle)),'<------->',"flexionado")
                
                if angle >= 120:
                    stage = "down"
                if angle < 40 and stage == "down":
                    stage = "up"
                    count += 1
                    print(str(count)) 
                    
            except:
                print("Donde andas?")
                
                
            mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2)
                                      ) #draw landmarks
            
            frame = imutils.resize(frame, width=320)
            return frame, count
            

if __name__ == "__main__":
    abdominal(cap,1280,720)