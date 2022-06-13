from flask import Flask, request, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append("../module")
from checkpoint import Checkpoints
from datetime import time, timedelta
from config import CheckInSystemConfig, Database
from flask_session import Session
from db_table import Employee, ClockRecord, Device

# Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Database.connect
db = SQLAlchemy(app)

#config session
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'HawaiiDream'
Session(app)

# checkpoint
checkpoints = Checkpoints(db)

@app.route("/")
def init():
    if not session.get("name"):
        return redirect("/login")
    return render_template("configPage.html", config = checkpoints.config, reports = checkpoints.scanner.queryall())

@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
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
    return render_template("configPage.html", config = checkpoints.config, reports = checkpoints.scanner.queryall())

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9122, debug=False)