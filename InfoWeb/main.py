from flask import Flask, request
import sys
sys.path.append("../module")
from db_table import EMPLOYEE, CLOCKRECORD
from scanner import Scanner
import socket

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
    if not db.session.query(EMPLOYEE.query.filter(EMPLOYEE.MAC == mac).exist()).scalar():
        employee = EMPLOYEE(name, mac, device)
        db.session.add(employee)
        db.session.commit()
    return name


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
