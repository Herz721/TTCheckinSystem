from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append("../module")
from checkpoint import Checkpoints
from datetime import time, timedelta
from config import CheckInSystemConfig
from db_table import EMPLOYEE, CLOCKRECORD
import socket
from flask_session import Session

# Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:********@localhost/TrojanTech'
db = SQLAlchemy(app)

# host ip
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

checkpoints = Checkpoints(db, ip)
app = Flask(__name__)

@app.route('/')
def init():
    # TODO:Add login redirect
    if not session.get("name"):
        return redirect("/login")
    return render_template("configPage.html", config = checkpoints.config)

@app.route("/login",methods = ["GET","POST"])
def login():
    if request.methods == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")

@app.route('/setTime', methods=['POST'])
def result():
    """
    Set checkin time and checkout time

    """
    print(request.form)
    checkpoints.config = CheckInSystemConfig(request.form["clockin"], request.form["clockout"])
    checkpoints.addTrigger()
    checkpoints.scheduler.print_jobs()
    return render_template("configPage.html", config = checkpoints.config)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9122, debug=False)
