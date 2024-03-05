import dotenv
import os
import psycopg2
import json
from flask import Flask, jsonify, make_response, Response
from functools import wraps
import cv2

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

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
    # FIXME: OpenCV와의 연동 필요
    width = 640
    height = 480
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print("Camera_Connected")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20,20))
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
            else:
                print("down")
        elif len(faces) == 0:
            print("Please see the camera correctly")
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()
    print("updown")
    return jsonify({"result": "success"})

@app.route('/api/pay', methods=['POST'])
def pay():
    # FIXME: Arduino와의 연동으로 카드 인식 필요
    if(True):
        return jsonify({"result": "success"})

@app.route('/api/age', methods=['GET'])
def get_age():
    # FIXME: OpenCV와의 연동 필요
    width = 640
    height = 480
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
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(frame, (x + w // 2, y + h // 2), 5, (0, 0, 255), -1)
            # print(x, y, w, h)
        if len(faces) > 0:
            MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
            age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
            age_net = cv2.dnn.readNetFromCaffe("deploy_age.prototxt", "age_net.caffemodel")
            for (x, y, w, h) in faces:
                face_img = frame[y:y, h:h + w].copy()
                print(face_img)
                # FIXME: OpenCV 에러 고쳐야 함.
                blob = cv2.dnn.blobFromImage(face_img, 1, (244, 244), MODEL_MEAN_VALUES, swapRB=True)
                age_net.setInput(blob)
                age_preds = age_net.forward()
                print(age_preds)

        elif len(faces) == 0:
            print("Face Doesn't Exists")
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()
    print("updown")
    return jsonify({"age": "20"})

if __name__ == '__main__':
    app.run(debug=True)