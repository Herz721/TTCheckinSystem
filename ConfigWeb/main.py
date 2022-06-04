from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append("../module")
from checkpoint import Checkpoints
from datetime import time, timedelta
from config import CheckInSystemConfig, Database
from db_table import EMPLOYEE, CLOCKRECORD
import socket

# Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Database.connect
db = SQLAlchemy(app)

# host ip
hostname = socket.getfqdn()
print(hostname)
ip = socket.gethostbyname(hostname)
print(ip)

checkpoints = Checkpoints(db, ip)
app = Flask(__name__)

@app.route('/')
def init():
    return render_template("configPage.html", config = checkpoints.config)


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
