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
app.config['WORD_FILES'] = Path('word_files')

CORS(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def homepage():
	return app.send_static_file("index.html")

@app.route('/schedule_duty',methods=['POST'])
def schedule_duty():
	payload = json.loads(request.data)
	scheduler = Scheduler(payload)
	scheduler.start_schedule()

	if payload['raDuty']:
		return send_from_directory(app.config['EXCEL_FILES'], scheduler.filename + ".xlsx", as_attachment=True)
	return send_from_directory(app.config['WORD_FILES'], scheduler.filename + ".docx", as_attachment=True)
if __name__ == "__main__":
	app.run(host='localhost', debug=True, port=8000)

