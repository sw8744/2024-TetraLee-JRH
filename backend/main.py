import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import time
import serial

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

width = 640
height = 480
ser = ""
isArduino = False
if input("Do you want to use Arduino? (y/n): ") == 'y':
    isArduino = True
    ser = input("Enter the serial port: ")

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

c = connection.cursor()
c.execute("SELECT * FROM food.food ORDER BY id")
menu = c.fetchall()
c.close()
print(menu)

@app.get('/api/start/{whereToEat}')
def start(whereToEat):
    if whereToEat not in ['eatIn', 'takeOut']:
        return HTTPException(400, 'whereToEat is not correct')

    where = ''
    if whereToEat == 'takeOut':
        where = "포장"
    elif whereToEat == 'eatIn':
        where = "매장"

    cur = connection.cursor()
    cur.execute("SELECT * FROM purchase.history ORDER BY id")
    result = cur.fetchall()

    num = len(result) + 1
    ordermenu = [0 for _ in range(len(menu))]

    cur.execute("INSERT INTO purchase.history (id, ordermenu, ispaid, date, wheretoeat) VALUES (%s, %s, %s, %s, %s)", (num, ordermenu, False, time.strftime('%Y-%m-%d %H:%M:%S'), where))
    connection.commit()
    cur.close()

    return {"order_num": num}

@app.get('/api/getinfo/{id}')
def get_info(id):
    id_int = int(id)

    cur = connection.cursor()
    cur.execute("SELECT * FROM purchase.history WHERE id = " + id + "ORDER BY id")
    result = cur.fetchall()
    result = result[0]
    cur.close()

    return {"id": result[0], "ordermenu": result[1], "ispaid": result[2], "date": result[3], "wheretoeat": result[4], "age": result[5]}

@app.post('/api/order/{id}/{menuId}/{amount}')
def order(id, menuId, amount):
    id_int = int(id)
    menu_id = int(menuId)

    cur = connection.cursor()
    cur.execute("SELECT * FROM purchase.history WHERE id = " + id + "ORDER BY id")
    result = cur.fetchall()
    result = result[0][1]
    result[menu_id - 1] = int(amount)
    cur.execute("UPDATE purchase.history SET ordermenu = %s WHERE id = %s", (result, id))
    connection.commit()
    cur.close()

    return {"result": "success"}

@app.get('/api/ordermenu/{id}')
def orderMenu(id):
    id_int = int(id)
    cur = connection.cursor()
    cur.execute("SELECT * FROM purchase.history WHERE id = " + id + "ORDER BY id")
    result = cur.fetchall()
    result = result[0][1]
    cur.close()

    res = []
    for i in range(len(result)):
        if result[i] != 0:
            res.append({
                "id": i,
                "name": menu[i][1],
                "amount": result[i],
                "image": menu[i][7],
                "price": menu[i][3]
            })

    return res

@app.post('/api/pay/{id}')
def pay(id):
    cur = connection.cursor()
    cur.execute("UPDATE purchase.history SET ispaid = %s WHERE id = %s", (True, id))
    connection.commit()
    cur.close()

    return {"result": "success"}

@app.get('/api/menu')
def get_menu():
    cur = connection.cursor()
    cur.execute("SELECT * FROM food.food ORDER BY id")
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
    menu = res

    return res

@app.get('/api/kind')
def get_kind():
    cur = connection.cursor()
    cur.execute("SELECT * FROM food.food ORDER BY id")
    result = cur.fetchall()
    cur.close()

    res = []
    for i in result:
        res.append(i[5])
    res = {'kind': res}

    return res

@app.get('/api/menu/{age}')
def get_recommend_menu(age):
    cur = connection.cursor()
    cur.execute("SELECT * FROM food.food WHERE recommendation = '" + age.upper() + "'" + "ORDER BY id")
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

@app.get('/api/menukind/{kind}')
def get_kind_menu(kind):
    cur = connection.cursor()
    cur.execute("SELECT * FROM food.food WHERE kind = '" + kind + "'" + "ORDER BY id")
    result = cur.fetchall()
    cur.close()

    return result

@app.get('/api/getfoodinfo/{id}')
def get_food_info(id):
    cur = connection.cursor()
    cur.execute("SELECT * FROM food.food WHERE id = " + id + "ORDER BY id")
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

@app.get('/api/getfoodamount/{id}/{foodId}')
def get_food_info(id, foodId):
    foodid_int = int(foodId) - 1
    cur = connection.cursor()
    cur.execute("SELECT * FROM purchase.history WHERE id = " + id + "ORDER BY id")
    result = cur.fetchall()
    cur.close()

    return {"amount": result[0][1][foodid_int]}

@app.post('/api/updown')
def updown():
    prev_pos = ""
    ageProto = 'age_deploy.prototxt'
    ageModel = 'age_net.caffemodel'
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    print("Camera_Connected")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 0 for finish acting
    if isArduino:
        ser_conn = serial.Serial(ser, 9600)
        while True:
            ser_conn.write(str.encode('0'))
            if ser_conn.readable():
                res = ser_conn.readline()
                if res == b'0':
                    break
            time.sleep(0.1)
        ser_conn.write(str.encode('3'))
        while True:
            if ser_conn.readable():
                res = ser_conn.readline()
                if res == b'0':
                    break
        ser_conn.write(str.encode('1'))
        while True:
            if ser_conn.readable():
                res = ser_conn.readline()
                if res == b'0':
                    break

    while True:
        ret, frame = capture.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
        x_f = 0; y_f = 0; w_f = 0; h_f = 0
        for (x, y, w, h) in faces:
            x_f = x; y_f = y; w_f = w; h_f = h
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.circle(frame, (x + w // 2, y + h // 2), 5, (0, 0, 255), -1)
            # 1 for up, 2 for stop, 3 for down
        if len(faces) > 0:
            if y_f + h_f // 2 < height // 3 * 2:
                print("middle")
                ser_conn.write(str.encode('2'))
                time.sleep(0.5)
                for (x, y, w, h) in faces:
                    face_img = frame[y:y, h:h + w].copy()
                    blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                    ageNet = cv2.dnn.readNet(ageModel, ageProto)
                    ageNet.setInput(blob)
                    agePreds = ageNet.forward()
                    age = ageList[agePreds[0].argmax()]

                    age_pred = age[1:-1]
                    if age_pred in ['(0-2)', '(4-6)', '(8-12)']:
                        cur = connection.cursor()
                        cur.execute("UPDATE purchase.history SET age = %s WHERE id = %s", ("YOUNG", id))
                        connection.commit()
                        cur.close()
                    elif age_pred in ['(15-20)', '(25-32)', '(38-43)', '(48-53)']:
                        cur = connection.cursor()
                        cur.execute("UPDATE purchase.history SET age = %s WHERE id = %s", ("MIDDLE", id))
                        connection.commit()
                        cur.close()
                    elif age_pred in ['(60-100)']:
                        cur = connection.cursor()
                        cur.execute("UPDATE purchase.history SET age = %s WHERE id = %s", ("OLD", id))
                        connection.commit()
                        cur.close()
                return {"result": "success"}
        elif len(faces) == 0:
            if prev_pos != "error":
                prev_pos = "error"
                print("Please see the camera correctly")
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # capture.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
