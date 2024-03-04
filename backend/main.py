import dotenv
import os
import psycopg2
import json
from flask import Flask, jsonify, make_response, Response
from functools import wraps

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