from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import sys
sys.path.append("../module")
from checkpoint import Checkpoints
from datetime import time, timedelta
from config import CheckInSystemConfig
from db_table import EMPLOYEE, CLOCKRECORD
import socket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:********@localhost/TrojanTech'
db = SQLAlchemy(app)


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

checkpoints = Checkpoints(ip)
app = Flask(__name__)

@app.route('/')
def init():
    return render_template("configPage.html", config = checkpoints.config)


@app.route('/setTime', methods=['POST'])
def result():
    print(request.form)
    checkpoints.config = CheckInSystemConfig(time(int(request.form["clockin"])), time(int(request.form["clockout"])))
    checkpoints.addTrigger()
    checkpoints.scheduler.print_jobs()
    return render_template("configPage.html", config = checkpoints.config)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
