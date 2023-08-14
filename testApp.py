from flask import Flask, render_template, Response
import imutils
import cv2
import scripts.squatsPro as sq
import scripts.abdominal as ab
import scripts.arm as arm
import scripts.pushUp as pu
import scripts.yoga as yg

app = Flask(__name__)
h = 480
w = 640
cap = cv2.VideoCapture("squats.mp4")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

def video(id):
    while True:
        if id == 1:
            #----------uyuyuyuy
            theVideo = sq.videoSquats(cap,w,h)
            theVideo = cv2.resize(theVideo,(0,0),fx=1,fy=1)
            
        encodedImg = cv2.imencode(".jpg",theVideo)[1].tobytes()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImg)+ b'\r\n')
        
@app.route('/<int:id>')
def index(id):
    return Response(video(id),mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/release')
def release_cap():
    cap.release()
    return "Camera Released"
    
if __name__ == "__main__":
    app.run(debug=True)