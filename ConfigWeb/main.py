from flask import Flask, request, render_template
import sys
sys.path.append("../module")
from checkpoint import Checkpoints
from datetime import time, timedelta

checkpoints = Checkpoints()
checkpoints.scheduler.print_jobs()
checkpoints.scheduler.start()
app = Flask(__name__)

@app.route('/')
def init():
    return render_template("configPage.html")


@app.route('/setTime')
def result():
    self.config.clockinTime = request.form["clockin"]
    self.config.clockoutTime = request.form["clockout"]
    return render_template("configPage.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
