from flask import Flask, request
from db_table import db_table
import os

app = Flask(__name__, static_url_path='')


@app.route('/')
def init():
    return app.send_static_file("index.html")


@app.route('/result')
def result():
    name = request.args.get('name')
    device = request.args.get('device')
    ip = request.remote_addr
    vals = (name, device, ip)
    db = db_table()
    db.insert("INSERT INTO EMPLOYEE (ENAME, IP, DEVICE) VALUES (%s, %s, %s);", vals)
    db.close()
    return name


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
