from flask import Flask, render_template, Response
import imutils
import cv2
import requests
import scripts.squatsPro as sq
import scripts.abdominal as ab
import scripts.arm as arm
import scripts.pushUp as pu
import scripts.yoga as yg

from kotlinTest.server import correos 

app = Flask(__name__)
h = 720
w = 1280
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
URL = 'https://mainapi-istq.onrender.com/exercises'

email = 'StandUser@gmail.com'

def video(id):
    while True:
        with open("kotlinTest/emails.txt", "r") as file:
            emails = [line.strip() for line in file]
        if id == 1:
            theVideo, count = sq.videoSquats(cap,w,h)
            if count == 10:
                obj = {'email':emails[-1],'typeOf':str(id),'count':str(count)}
                print("a")
                requests.post(URL,json=obj)
                count = 0
            theVideo = cv2.resize(theVideo,(0,0),fx=1,fy=1)
        if id == 2:
            theVideo,count = ab.abdominal(cap,w,h)
            if count == 10:
                obj = {'email':emails[-1],'typeOf':str(id),'count':str(count)}
                requests.post(URL,json=obj)
                count = 0
            theVideo = cv2.resize(theVideo,(0,0),fx=1,fy=1)
        if id == 3:
            theVideo,count = arm.armVideo(cap,w,h)
            if count == 10:
                obj = {'email':emails[-1],'typeOf':str(id),'count':str(count)}
                requests.post(URL,json=obj)
                count = 0
            theVideo = cv2.resize(theVideo,(0,0),fx=1,fy=1)
        if id == 4:
            theVideo, count = pu.pushUp(cap,w,h)
            if count == 10:
                obj = {'email':emails[-1],'typeOf':str(id),'count':str(count)}
                requests.post(URL,json=obj)
                count = 0
            theVideo = cv2.resize(theVideo,(0,0),fx=1,fy=1)
        if id == 5:
            theVideo, count = yg.yoga(cap,w,h)
            if count == 10:
                obj = {'email':emails[-1],'typeOf':str(id),'count':str(count)}
                requests.post(URL,json=obj)
                count = 0
            theVideo = cv2.resize(theVideo,(0,0),fx=1,fy=1)
            
        encodedImg = cv2.imencode(".jpg",theVideo)[1].tobytes()
        (f,encodedImg) = cv2.imencode(".jpg",theVideo)
        if not f:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImg)+ b'\r\n')
        
@app.route('/<int:id>')
def index(id):
    return Response(video(id),mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="192.168.0.3",debug=True)