from flask import Flask, request
import sys
sys.path.append("../module")
from db_table import Employee, ClockRecord, Device
from config import Database
from flask_sqlalchemy import SQLAlchemy
from scanner import Scanner

# create database
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = Database.connect
db = SQLAlchemy(app)

scanner = Scanner(db)

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
    if db.session.query(Device).filter_by(MAC = mac).first() == None:
        employee = db.session.query(Employee).filter_by(ename = name).first()
        device = Device(mac, "phone", name + "'s phone", employee.eid)
        db.session.add(device)
        db.session.commit()
        db.session.flush()
    return name

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9222, debug=False)
