import dotenv
import os
import psycopg2
import json
from flask import Flask, jsonify, make_response

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


@app.route('/api/menu', methods=['GET'])
def get_menu():
    # FIXME: 인코딩 오류 고칠 필요 있음.
    cur = connection.cursor()
    cur.execute("SELECT * FROM " + os.environ.get("TABLE_NAME"))
    fetch = cur.fetchall()
    res = json.dumps(fetch, ensure_ascii=False, indent=4)
    res = json.loads(res)
    print(type(res))
    cur.close()
    return res

@app.route('/api/menu/<age>', methods=['GET'])
def get_recommend_menu(age):
    cur = connection.cursor()
    cur.execute("SELECT * FROM " + os.environ.get("TABLE_NAME") + " WHERE recommendation = '" + age.upper() + "'")
    res = json.dumps(cur.fetchall(), ensure_ascii=False, indent=4)
    res = make_response(res)
    cur.close()
    return res

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