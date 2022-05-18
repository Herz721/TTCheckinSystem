from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__, static_url_path='')
COLUMNS = ['name', 'device', 'ip']

@app.route('/')
def init():
    return app.send_static_file("index.html")

@app.route('/result')
def result():
    if(os.path.isfile('localStorage.csv')):
        df = pd.read_csv('localStorage.csv')
        print(df)
    else:
        df = pd.DataFrame(columns = COLUMNS)
        print(df)
    name = request.args.get('name')
    device = request.args.get('equipment')
    ip = request.remote_addr
    newData = pd.DataFrame({'name': name, 'device': device, 'ip': ip}, index=[1])
    df = pd.concat([df, newData], ignore_index=True)
    df.drop_duplicates(subset = ['ip'], keep = 'last', inplace = True)
    df.to_csv('localStorage.csv', index = 0)
    return name

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug = True)