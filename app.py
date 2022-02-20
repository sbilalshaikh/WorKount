from importlib.metadata import requires
from werkzeug import Response
from flask import Flask, redirect, render_template, url_for, request
import cv2

app = Flask(__name__)

cam = cv2.VideoCapture(0)

reps = 0
sets = 0
excercise = ''
time = 0

def captureFrame():
    while True:            
        success, frame = cam.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()

    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    global reps, sets, pause, excercise

    if request.method == 'POST':
        reps = request.form['reps']
        sets = request.form['sets']
        pause = request.form['pause']
        excercise = request.form['excerise']

        return redirect(url_for('repCounter'))
    return render_template('initial.html')

@app.route('/reps')
def repCounter():
    return render_template('index.html', reps=reps, sets=sets, pause=pause, excercise=excercise)

@app.route('/video')
def video():
    return Response(captureFrame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)