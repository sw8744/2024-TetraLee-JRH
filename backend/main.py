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
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20,20))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
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
    return jsonify({"age": "20"})

if __name__ == '__main__':
    app.run(debug=True)