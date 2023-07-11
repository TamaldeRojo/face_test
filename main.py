from scripts.abdominal import abdominal
from scripts.arm import armVideo
from scripts.pushUp import pushUp
from scripts.squatsPro import videoSquats
from scripts.yoga import yoga
import cv2,mediapipe as mp, numpy as np, math 

#cap = cv2.VideoCapture(0)
recivedValue = int(input("Ingresa un numero: "))

def programSetup(i):
    if i == 1:
        cap = cv2.VideoCapture("situps.mp4")
        print("Abdominales")
        abdominal(cap)
    elif i == 2:
        cap = cv2.VideoCapture("pushup.mp4")
        print("Lagartijas")
        pushUp(cap)
    elif i == 3:
        cap = cv2.VideoCapture("arm.mp4")
        print("Brazo")
        armVideo(cap)
    elif i == 4:
        cap = cv2.VideoCapture("squats.mp4")
        print("Sentadillas")
        videoSquats(cap)
    elif i == 5:
        cap = cv2.VideoCapture("yoga.mp4")
        print("Yoga")
        yoga(cap)
    else:
        return "Ese numero no bro: "
     

if __name__ == "__main__":
    programSetup(recivedValue)