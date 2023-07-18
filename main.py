from scripts.abdominal import abdominal
from scripts.arm import armVideo
from scripts.pushUp import pushUp
from scripts.squatsPro import videoSquats
from scripts.yoga import yoga
import cv2,mediapipe as mp, numpy as np, math, pickle ,struct

import socket
import threading

#Por paquete debo recibir:
# Width,Height
# Num Protocolo (1,..,5)
#Debe Enviar:
# Video 
#host_name = socket.gethostname()
#SERVER = socket.gethostbyname(host_name)



def get_width_height():
    pass
w,h = 1280,720 

def programSetup(cap,i,w,h):
    if i == 1:
        #cap = cv2.VideoCapture("situps.mp4")
        print("Abdominales")
        abdominal(cap,w,h)
    elif i == 2:
        #cap = cv2.VideoCapture("pushup.mp4")
        print("Lagartijas")
        pushUp(cap,w,h)
    elif i == 3:
        #cap = cv2.VideoCapture("arm.mp4")
        print("Brazo")
        frame = armVideo(cap,w,h)#test--------------------------->
    elif i == 4:
        #cap = cv2.VideoCapture("squats.mp4")
        print("Sentadillas")
        videoSquats(cap,w,h)
    elif i == 5:
        #cap = cv2.VideoCapture("legs.mp4")
        print("legs")
        yoga(cap,w,h)
    else:
        return print("Saliendo...")
    
    return frame #test--------------------------->
     
def getKey(conn) -> int:
    print("Looking for a key number")
    while True:
        data = conn.recv(1024)  # Receive data from client
        if not data:
            break
        number = int(data.decode())
        if 1 <= number <= 5:
            print(f"Received valid number: {number}")
            return number
        else:
            print(f"Received invalid number: {number}")
            break
    #conn.close()
    

if __name__ == "__main__":
    PORT = 5050
    SERVER = "192.168.56.1" #cambiar en raspberry
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    
    print("[+] Server is starting...")
    print(f'HOST IP: {SERVER}')
    print(f"LISTENING AT: {ADDR}")
    
    
    while True:
        client_socket,addr = server.accept()
        print(f'GOT CONNECTION FROM: {addr}')
        if client_socket:
            cap = cv2.VideoCapture(0)
                
            key = getKey(client_socket) #Protocolo ejercicio
            print(f"Tengo {key}")
            try:
                while cap.isOpened():
                    frame = programSetup(cap,key,640,480)
                    cv2.imshow("server",frame)
                    a = pickle.dumps(frame)
                    message = struct.pack('Q',len(a))+a 
                    #client_socket.sendall(message)
            except:
                cap.release()
                client_socket.close()
                print("[+] ENDING...")
                break
            
    