import psycopg2
import json
from flask import Flask, jsonify, make_response, Response
from functools import wraps
import cv2
import time
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={
  r"/api/*": {"origin": "*"},
})

width = 640
height = 480
ser = 'COM3'

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

connection = psycopg2.connect(
    host="osu-api.kro.kr",
    database="kiosk",
    port=5432,
    user="jrh",
    password="ishs12345!"
    )
print("DB_Connected")

def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

@app.route('/api/start/<whereToEat>', methods=['POST'])
def start(whereToEat):
    cur = connection.cursor()
    cur.execute("SELECT * FROM purchase.history")
    result = cur.fetchall()
    cur.execute("INSERT INTO purchase.history (id, ordermenu, ispaid, date, wheretoeat) VALUES (%s, %s, %s, %s, %s)", (len(result) + 1, [], False, time.strftime('%Y-%m-%d %H:%M:%S'), whereToEat))
    connection.commit()
    cur.close()
    return make_response(jsonify({"result": "success"}), 200)

@app.route('/api/order/<id>/<menu>', methods=['POST'])
def order(id, menu):
    cur = connection.cursor()
    cur.execute("SELECT * FROM purchase.history WHERE id = " + id)
    result = cur.fetchall()
    ordermenu = result[0][1]
    if menu in ordermenu:
        ordermenu[menu] += 1
    else:
        ordermenu[menu] = 1
    cur.execute("UPDATE purchase.history SET ordermenu = %s WHERE id = %s", (ordermenu, id))
    connection.commit()
    cur.close()
    return make_response(jsonify({"result": "success"}), 200)

@app.route('/api/menu', methods=['GET'])
@as_json
def get_menu():
    cur = connection.cursor()
    cur.execute("SELECT * FROM food.food")
    result = cur.fetchall()
    cur.close()
    res = []
    for i in result:
        res.append({
            "id": i[0],
            "name": i[1],
            "description": i[2],
            "caution": i[8],
            "price": i[3],
            "recommendation": i[4],
            "kind": i[5],
            "selling": i[6],
            "image": i[7]
        })
    return res

@app.route('/api/kind', methods=['GET'])
@as_json
def get_kind():
    cur = connection.cursor()
    cur.execute("SELECT * FROM food.food")
    result = cur.fetchall()
    cur.close()
    res = []
    for i in result:
        res.append(i[5])
    res = {'kind': res}
    return res

@app.route('/api/menu/<age>', methods=['GET'])
@as_json
def get_recommend_menu(age):
    cur = connection.cursor()
    cur.execute("SELECT * FROM food.food WHERE recommendation = '" + age.upper() + "'")
    result = cur.fetchall()
    cur.close()
    res = []
    for i in result:
        res.append({
            "id": i[0],
            "name": i[1],
            "description": i[2],
            "caution": i[8],
            "price": i[3],
            "recommendation": i[4],
            "kind": i[5],
            "selling": i[6],
            "image": i[7]
        })
    return res

@app.route('/api/menu/<kind>', methods=['GET'])
@as_json
def get_kind_menu(kind):
    cur = connection.cursor()
    cur.execute("SELECT * FROM food.food WHERE kind = '" + kind + "'")
    result = cur.fetchall()
    cur.close()
    return result

@app.route('/api/updown', methods=['GET'])
def updown():
    prev_pos = ""
    ageProto = 'age_deploy.prototxt'
    ageModel = 'age_net.caffemodel'
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    print("Camera_Connected")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        # ser_conn = serial.Serial(ser, 9600)
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
        x_f = 0; y_f = 0; w_f = 0; h_f = 0
        for (x, y, w, h) in faces:
            x_f = x; y_f = y; w_f = w; h_f = h
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.circle(frame, (x + w // 2, y + h // 2), 5, (0, 0, 255), -1)
            # print(x, y, w, h)
            # 0 for stop, 1 for up, 2 for down
        if len(faces) > 0:
            if y_f + h_f // 2 < height // 3:
                if prev_pos != "up":
                    prev_pos = "up"
                    print("up")
                    # ser_conn.write(str.encode('1'))
            elif y_f + h_f // 2 < height // 3 * 2:
                print("middle")
                time.sleep(0.5)
                for (x, y, w, h) in faces:
                    face_img = frame[y:y, h:h + w].copy()
                    blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                    ageNet = cv2.dnn.readNet(ageModel, ageProto)
                    ageNet.setInput(blob)
                    agePreds = ageNet.forward()
                    age = ageList[agePreds[0].argmax()]
                    # ser_conn.write(str.encode('0'))
                    age_pred = age[1:-1]
                    if age_pred in ['(0-2)', '(4-6)', '(8-12)']:
                        return make_response(jsonify({"age": age_pred, "ageType": 'YOUNG'}, 200))
                    elif age_pred in ['(15-20)', '(25-32)', '(38-43)', '(48-53)']:
                        return make_response(jsonify({"age": age_pred, "ageType": 'MIDDLE'}, 200))
                    elif age_pred in ['(60-100)']:
                        return make_response(jsonify({"age": age_pred, "ageType": 'OLD'}, 200))
                return make_response(jsonify({"result": "success"}), 200)
            else:
                if prev_pos != "down":
                    prev_pos = "down"
                    print("down")
                    # ser_conn.write(str.encode('2'))
        elif len(faces) == 0:
            if prev_pos != "error":
                prev_pos = "error"
                print("Please see the camera correctly")
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # capture.release()
    # cv2.destroyAllWindows()

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
                age_pred = age[1:-1]
                if age_pred in ['(0-2)', '(4-6)', '(8-12)']:
                    return make_response(jsonify({"age": age_pred, "ageType": 'YOUNG'}, 200))
                elif age_pred in ['(15-20)', '(25-32)', '(38-43)', '(48-53)']:
                    return make_response(jsonify({"age": age_pred, "ageType": 'MIDDLE'}, 200))
                elif age_pred in ['(60-100)']:
                    return make_response(jsonify({"age": age_pred, "ageType": 'OLD'}, 200))
        elif len(faces) == 0:
            print("Face Doesn't Exists")
            return make_response(jsonify({"Error": "Face Doesn't Exists"}), 404)
        cv2.imshow('frame', frame)
    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(debug=True)