import cv2,mediapipe as mp, numpy as np,math, imutils


cap = cv2.VideoCapture("pushup.mp4")

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

stage = None
count = 0

def pushUp(cap,w,h):
    global stage,count
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as Pose:
        
        frame_count = 0
        frames_to_skip = 5
        while cap.isOpened():
            
            frame_count += 1
            success,frame = cap.read()
            if not success:
                break 
            if frame_count % frames_to_skip != 0:
                    continue
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False 

            frame = cv2.flip(frame,1)
            results = Pose.process(frame)

            frame.flags.writeable = True 
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            try:
                landmarks = results.pose_landmarks.landmark
                
                Nose = [int(landmarks[0].x*w),int(landmarks[0].y*h)]
                
                midShoulder = [
                    int(((landmarks[11].x + landmarks[12].x)/2) * w),
                    int(((landmarks[11].y + landmarks[12].y)/2) * h )
                        ]
                midWrists = [
                    int(((landmarks[15].x + landmarks[16].x)/2) * w),
                    int(((landmarks[15].y + landmarks[16].y)/2) * h )
                        ]
                #print("a")
                image = np.zeros((h,w,3),dtype=np.uint8)
                frame = cv2.circle(image,(midShoulder[0],midShoulder[1]),1,(102,255,105),10)
                frame = cv2.circle(image,(midWrists[0],midWrists[1]),1,(102,255,105),10)
                frame = cv2.circle(image,(Nose[0],Nose[1]),1,(102,255,105),10)
                
                distance_shoulder_wrist = int(math.sqrt(((midWrists[0]-midShoulder[0])**2) + ((midWrists[1]-midShoulder[1])**2)))
                #print(distance_shoulder_wrist)
                
                if distance_shoulder_wrist >= 240:
                    stage = 'up'
                if distance_shoulder_wrist <= 190 and stage == 'up':
                    stage = 'down'
                    count += 1
                    print(str(count),"------------------")
                
                
                
                
            except:
                print("Uwu")
                
            mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2)
                                      ) #draw landmarks
            frame = imutils.resize(frame, width=320)
            return frame, count

if __name__ == '__main__':
    pushUp(cap,1280,720)