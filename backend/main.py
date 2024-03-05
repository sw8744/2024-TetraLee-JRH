import dotenv
import os
import psycopg2
import json
from flask import Flask, jsonify, make_response, Response
from functools import wraps
import cv2
import time

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

width = 640
height = 480

connection = psycopg2.connect(
    host="osu-api.kro.kr",
    database=os.environ.get("DB_NAME"),
    port=int(os.environ.get("DB_PORT")),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD")
    )
print("DB_Connected")

def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

@app.route('/api/menu', methods=['GET'])
@as_json
def get_menu():
    cur = connection.cursor()
    cur.execute("SELECT * FROM " + os.environ.get("TABLE_NAME"))
    result = cur.fetchall()
    cur.close()
    return result

@app.route('/api/menu/<age>', methods=['GET'])
@as_json
def get_recommend_menu(age):
    cur = connection.cursor()
    cur.execute("SELECT * FROM " + os.environ.get("TABLE_NAME") + " WHERE recommendation = '" + age.upper() + "'")
    result = cur.fetchall()
    cur.close()
    return result

@app.route('/api/updown', methods=['POST'])
def updown():
    # FIXME: Arduino와의 연동 필요
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print("Camera_Connected")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
        x_f = 0; y_f = 0; w_f = 0; h_f = 0
        for (x, y, w, h) in faces:
            x_f = x; y_f = y; w_f = w; h_f = h
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.circle(frame, (x + w // 2, y + h // 2), 5, (0, 0, 255), -1)
            # print(x, y, w, h)
        if len(faces) > 0:
            if y_f + h_f // 2 < height // 3:
                print("up")
            elif y_f + h_f // 2 < height // 3 * 2:
                print("middle")
                return make_response(jsonify({"result": "success"}), 200)
            else:
                print("down")
        elif len(faces) == 0:
            print("Please see the camera correctly")
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()


@app.route('/api/pay', methods=['POST'])
def pay():
    # FIXME: Arduino와의 연동으로 카드 인식 필요
    if(True):
        return make_response(jsonify({"result": "success"}), 200)

@app.route('/api/age', methods=['GET'])
def get_age():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print("Camera_Connected")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    ageProto = 'age_deploy.prototxt'
    ageModel = 'age_net.caffemodel'
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    max_time_end = time.time() + 3
    ages = []
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
        x_f = 0; y_f = 0; w_f = 0; h_f = 0
        for (x, y, w, h) in faces:
            x_f = x; y_f = y; w_f = w; h_f = h
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(frame, (x + w // 2, y + h // 2), 5, (0, 0, 255), -1)
            # print(x, y, w, h)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face_img = frame[y:y, h:h + w].copy()
                blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                ageNet = cv2.dnn.readNet(ageModel, ageProto)
                ageNet.setInput(blob)
                agePreds = ageNet.forward()
                age = ageList[agePreds[0].argmax()]
                return make_response(jsonify({"age": age[1:-1]}), 200)
        elif len(faces) == 0:
            print("Face Doesn't Exists")
            return make_response(jsonify({"Error": "Face Doesn't Exists"}), 404)
        cv2.imshow('frame', frame)
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(debug=True)