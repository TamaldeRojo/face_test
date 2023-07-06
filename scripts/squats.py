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

def videoSquats():
        global count
        global down
        global up
        with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5,static_image_mode=False) as pose:
            
            while True:
                
                success, frame = cap.read()
                if not success:
                    break
                frame = cv2.flip(frame,1)
                h,w,_ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks is not None:

                    xNose = int(results.pose_landmarks.landmark[0].x * w)
                    yNose = int(results.pose_landmarks.landmark[0].y * h)

                    cv2.circle(frame, (xNose,yNose),6,(0,255,255),4)

                    #left -------------------------------------->
                    x1 = int(results.pose_landmarks.landmark[24].x * w)
                    y1 = int(results.pose_landmarks.landmark[24].y * h)

                    x2 = int(results.pose_landmarks.landmark[26].x * w)
                    y2 = int(results.pose_landmarks.landmark[26].y * h)

                    x3 = int(results.pose_landmarks.landmark[28].x * w)
                    y3 = int(results.pose_landmarks.landmark[28].y * h)

                
                    #circles
                    aux_img = np.zeros(frame.shape, np.uint8)
                    cv2.line(aux_img,(x1,y1),(x2,y2),(255,255,0),4)
                    cv2.line(aux_img,(x2,y2),(x3,y3),(255,255,0),4)
                    cv2.line(aux_img,(x1,y1),(x3,y3),(255,255,0),4)
                    

                    cv2.circle(frame, (x1,y1),6,(0,255,255),4)
                    cv2.circle(frame, (x2,y2),6,(128,0,250),4)
                    cv2.circle(frame, (x3,y3),6,(128,0,250),4)

                    #end left -------------------------------------->

                    #right
                    x4 = int(results.pose_landmarks.landmark[23].x * w)
                    y4 = int(results.pose_landmarks.landmark[23].y * h)

                    x5 = int(results.pose_landmarks.landmark[25].x * w)
                    y5 = int(results.pose_landmarks.landmark[25].y * h)

                    x6 = int(results.pose_landmarks.landmark[27].x * w)
                    y6 = int(results.pose_landmarks.landmark[27].y * h)

                    #circles
                    cv2.line(aux_img,(x4,y4),(x5,y5),(255,255,0),4)
                    cv2.line(aux_img,(x5,y5),(x6,y6),(255,255,0),4)
                    cv2.line(aux_img,(x4,y4),(x6,y6),(255,255,0),4)
                    

                    cv2.circle(frame, (x4,y4),6,(0,255,255),4)
                    cv2.circle(frame, (x5,y5),6,(128,0,250),4)
                    cv2.circle(frame, (x6,y6),6,(128,0,250),4)

                    if yNose >= 10:
                        #print("Nariz altura---> "+str(yNose))
                        cv2.line(aux_img,(x1,y1),(x2,y2),(255,0,0),4)
                        cv2.line(aux_img,(x2,y2),(x3,y3),(255,0,0),4)
                        cv2.line(aux_img,(x1,y1),(x3,y3),(255,0,0),4)
                        cv2.line(aux_img,(x4,y4),(x5,y5),(255,0,0),4)
                        cv2.line(aux_img,(x5,y5),(x6,y6),(255,0,0),4)
                        cv2.line(aux_img,(x4,y4),(x6,y6),(255,0,0),4)  

                        
                        #calculando angulo
                        p1 = np.array([x1,y1])
                        p2 = np.array([x2,y2])
                        p3 = np.array([x3,y3])

                        l1 = np.linalg.norm(p2-p3)
                        l2 = np.linalg.norm(p1-p3)
                        l3 = np.linalg.norm(p1-p2)

                        angle = degrees(acos((l1**2+l3**2-l2**2)/(2*l1*l3)))


                    
                        if angle >= 150:
                            up = True #parado

                        if up == True and down == False and angle <= 149 and angle>=51:
                            down = True #flexionado
                        
                        if up == True and down == True and angle >= 50:
                            count += 1
                            up = False
                            down = False
                        print("Angulo:",str(int(angle)),"Total ---->",str(count))

                        
                            
                        
                    else:
                        print("Demasiado cercas, alejate un poco")
                        angle = 0
                        #calculando angulo
                        p1 = np.array([x1,y1])
                        p2 = np.array([x2,y2])
                        p3 = np.array([x3,y3])

                        l1 = np.linalg.norm(p2-p3)
                        l2 = np.linalg.norm(p1-p3)
                        l3 = np.linalg.norm(p1-p2)

                        angle = degrees(acos((l1**2+l3**2-l2**2)/(2*l1*l3)))




                    output = cv2.addWeighted(frame, 1,aux_img,0.8,0)
                    cv2.putText(output,str(int(angle)),(x2+30,y2),1,1.5,(128,0,250),2)
                    
                    return output
def release_camera():
        cap.release()
        cv2.destroyAllWindows()            
if __name__ == "__main__":
    videoSquats(cap)
    release_camera()