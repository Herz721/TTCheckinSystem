from flask import Flask, request
import sys
sys.path.append("../module")
from db_table import EMPLOYEE, CLOCKRECORD
from flask_sqlalchemy import SQLAlchemy
from scanner import Scanner
import socket

# create database
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:********@localhost/TrojanTech'
db = SQLAlchemy(app)

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
scanner = Scanner(ip)

def findMac(ip, ipdict):
    if ip in ipdict.keys():
        return ipdict[ip]
    else:
        print("find MAC failure")
        return ""

@app.route('/')
def init():
    return app.send_static_file("index.html")


@app.route('/result')
def result():
    name = request.args.get('name')
    device = request.args.get('device')
    ip = request.remote_addr
    mac = ""
    while mac == "":
        ipdict = scanner.findIpDict()
        print(ipdict)
        print(len(ipdict))
        mac = findMac(ip, ipdict)
    print(db.session.query(EMPLOYEE).filter_by(MAC = mac).first())
    if db.session.query(EMPLOYEE).filter_by(MAC = mac).first() == None:
        employee = EMPLOYEE(name, mac, device)
        db.session.add(employee)
        db.session.commit()
        db.session.flush()
    return name


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9886, debug=False)
