from scripts.abdominal import abdominal
from scripts.arm import armVideo
from scripts.pushUp import pushUp
from scripts.squatsPro import videoSquats
from scripts.yoga import yoga
import cv2,mediapipe as mp, numpy as np, math 

#cap = cv2.VideoCapture(0)

#Por paquete debo recibir:
# Width,Height
# Num Protocolo (1,..,5)


w,h = 1280,720

def programSetup():
    i = int(input("Ingresa un numero: "))
    if i == 1:
        cap = cv2.VideoCapture("situps.mp4")
        print("Abdominales")
        abdominal(cap,w,h)
    elif i == 2:
        cap = cv2.VideoCapture("pushup.mp4")
        print("Lagartijas")
        pushUp(cap,w,h)
    elif i == 3:
        cap = cv2.VideoCapture("arm.mp4")
        print("Brazo")
        armVideo(cap,w,h)
    elif i == 4:
        cap = cv2.VideoCapture("squats.mp4")
        print("Sentadillas")
        videoSquats(cap,w,h)
    elif i == 5:
        cap = cv2.VideoCapture("legs.mp4")
        print("legs")
        yoga(cap,w,h)
    elif i == 6:
        return print("Saliendo...")
    else:
        print("[-] Elige otro numero: ")
        return programSetup()
     

if __name__ == "__main__":
    programSetup()