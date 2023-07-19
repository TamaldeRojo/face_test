import socket,cv2,pickle,struct,mediapipe as mp, numpy as np,time
from math import degrees,acos
import sys
import os
import fcntl
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','scripts')))
from arm import armVideo as arm
from abdominal import abdominal
from pushUp import pushUp
from squatsPro import videoSquats
from yoga import yoga

 
def get_ip_address(ifname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            sock.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
    except IOError:
        ip_address = None
    return ip_address

HOST = get_ip_address('wlan0')
port = 5050
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
w = 640
h = 480

def connServer(host_ip,port):
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print(f"HOST IP: {host_ip}")

    socket_addr = (host_ip,port)
    server_socket.bind(socket_addr)
    server_socket.listen(5) #5 is the number of connections
    print(f"LISTENING AT: {socket_addr}")
    
    return server_socket

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

def setup(cap,i,w,h):
    time.sleep(5)
    if i == 1:
        #cap = cv2.VideoCapture("situps.mp4")
        print("Abdominales")
        frame = abdominal(cap,w,h)
    elif i == 2:
        #cap = cv2.VideoCapture("pushup.mp4")
        print("Lagartijas")
        frame = pushUp(cap,w,h)
    elif i == 3:
        #cap = cv2.VideoCapture("arm.mp4")
        #print("Brazo")
        frame = arm(cap,w,h)#test--------------------------->
    elif i == 4:
        #cap = cv2.VideoCapture("squats.mp4")
        print("Sentadillas")
        frame = videoSquats(cap,w,h)
    elif i == 5:
        #cap = cv2.VideoCapture("legs.mp4")
        print("legs")
        frame = yoga(cap,w,h)
    else:
        return print("Saliendo...")
    
    return frame #test--------------------------->
  
def runSetup(ss,cap):
    while True:
        client_socket,addr = ss.accept()
        print(f"GOT CONNECTION FROM: {addr}")
        if not client_socket:
            break
        #Arm Script
        num = getKey(client_socket)
        while cap.isOpened():
            
            frame = setup(cap,num,w,h)
            a = pickle.dumps(frame)
            message = struct.pack('Q',len(a))+a
            client_socket.sendall(message)
            cv2.imshow("ServerTest",frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                client_socket.close()
                cap.release()
                break
            

if __name__ == "__main__":
    server_socket = connServer(HOST,port)
    runSetup(server_socket,cap)
    pass