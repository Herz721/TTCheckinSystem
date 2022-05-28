from flask import Flask, request, render_template
import sys
sys.path.append("../module")
from checkpoint import Checkpoints
from datetime import time, timedelta
import socket

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
    checkpoints = Checkpoints(ip, request.form["clockin"], request.form["clockout"])
    return render_template("configPage.html", config = checkpoints.config)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
