import time
import json

from flask_apscheduler import APScheduler
from flask_cors import CORS 
from flask import Flask, request, make_response, redirect, url_for, send_from_directory, send_file

from backend.scheduler import Scheduler

from pathlib import Path
from datetime import datetime, timedelta
from pprint import pprint

app = Flask(__name__, static_folder='../my-app/build', static_url_path='/')
app.config['EXCEL_FILES'] = Path('excel_files')
CORS(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def homepage():
	return app.send_static_file("index.html")

@app.route('/schedule_duty',methods=['POST'])
def schedule_duty():
	scheduler = Scheduler(json.loads(request.data))
	scheduler.start_schedule()
	return send_from_directory(app.config['EXCEL_FILES'], scheduler.filename + ".xlsx", as_attachment=True)

if __name__ == "__main__":
	app.run(host='localhost', debug=True, port=8000)

