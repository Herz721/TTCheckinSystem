from flask import Flask, request, render_template, jsonify, json 
import sys
sys.path.append("../module")
from db_table import Employee, ClockRecord, Device
from config import Database
from flask_sqlalchemy import SQLAlchemy
from scanner import Scanner
from wtforms import SelectField
from flask_wtf import FlaskForm
from sqlalchemy import func, distinct

# create database
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = Database.connect
app.config['SECRET_KEY'] = 'HawaiianDream'
db = SQLAlchemy(app)

scanner = Scanner(db)

def findMac(ip, ipdict):
    if ip in ipdict.keys():
        return ipdict[ip]
    else:
        print("find MAC failure")
        return ""

class Form(FlaskForm):
    dpt = SelectField('Department', choices=[])
    name = SelectField('Name', choices=[])

@app.route('/', methods=['GET','POST'])
def init():
    form = Form()
    list_ = [one.dept for one in db.session.query(Employee.ename,Employee.dept).distinct(Employee.dept)]
    se = set(list_)
    li = list(se)
    form.dpt.choices = li
    # return app.send_static_file("index.html")
    if request.method == 'POST':
        name = db.session.query(Employee).filter_by(id=form.name.data).first()
        # dpt = db.session.query(Employee).filter_by(id=form.dpt.data).first()
        return '<h1>Department : {}, Name: {}'.format(dpt.id, name.id)
    return render_template("index.html",form=form)

@app.route('/name/<get_name>')
def nameByDept(get_name):
    names = db.session.query(Employee).filter_by(dept=get_name).all()
    nameList = []
    for person in names:
        nameObj = {}
        nameObj['id'] = person.eid
        nameObj['name'] = person.ename
        nameList.append(nameObj)
    return jsonify({'names': nameList})

@app.route('/result',methods=['GET','POST'])
def result():
    name_eid = request.form.get('name')
    device = request.form.get('device')
    dev_name = request.form.get('dev_name')
    ip = request.remote_addr
    mac = ""
    # print(",Name: " + name + ",Device: " + device + ",Device Name: " + dev_name)

    while mac == "":
        ipdict = scanner.findIpDict()
        print(ipdict)
        print(len(ipdict))
        mac = findMac(ip, ipdict)

    if mac = "":
        # meizhaodao
    elif db.session.query(Device).filter_by(MAC = mac).first() == None:
        # try
        # employee = db.session.query(Employee).filter_by(ename = name).first()
        device = Device(mac, device, dev_name, name_eid)
        db.session.add(device)
        db.session.commit()
        db.session.flush()
    # else:
        # TODO:Insert success or failed
    return name_eid

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9222, debug=True)
