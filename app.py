from flask import Flask, render_template, Response 
import cv2
import scripts.squats as sq



app = Flask(__name__)


def video():
    while True:
        (f,encodedImg) = cv2.imencode(".jpg",sq.videoSquats())
        if not f:
            continue
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImg)+ b'\r\n')
    sq.release_camera()



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/video_feed")
def video_feed():
    return Response(video(),mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="127.0.0.1",debug=True)