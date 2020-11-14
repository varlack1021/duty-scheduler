import time
import json

from flask_apscheduler import APScheduler
from flask_cors import CORS 
from flask import Flask, request, make_response, redirect, url_for, send_from_directory, send_file

from duty_sms_notifications import send_text_notification
from google_auth import get_event_dates, get_auth_url, callback, add_events
from scheduler import start_schedule, get_duty_dates_from_sheet

from datetime import datetime, timedelta
from pprint import pprint

app = Flask(__name__)
app.config['EXCEL_FILES'] = "C:/Users/Varla/Documents/Programming/Projects/Duty Scheduler"
CORS(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/download')
def download():
	return send_file('C:/Users/Varla/Documents/Programming/Tools/hadoop/wikiHadoop.txt', 'wikiHadoop.txt')
	
@app.route('/')
def home():
	return 'Connection'

@app.route('/help')
def helpfunc():
	#print(app.apscheduler.get_job(id='localhost'))
	#help(app.apscheduler)
	return 'Connected'

@app.route('/delete_cookies')
def delete_cookies():
	res = make_response('Removed cookies')
	for key in request.cookies:
		res.delete_cookie(key)
	return res
	

@app.route('/googlecallback', methods=['GET'])						
def googleCallBack():
	auth_response = request.url
	creds = callback(auth_response)
	res = make_response('Setting cookies')
	
	for key, value in creds.items():
		
		if type(value) is list:
			value = value[0]
		
		res.set_cookie(key, value, max_age=60*60*24*365*2)

	res.headers['location'] = url_for('add_duty_to_calendar')

	return res, 302

@app.route('/check_cookies', methods=['GET'])
def check_cookies():
	if not request.cookies.get('token'):
		return redirect(get_auth_url())

	return redirect(url_for('add_duty_to_caledar'))

@app.route('/schedule_events', methods=['GET'])
def schedule_events():	
	creds = request.cookies
	#number = request.args['number']
	#events = list(map(str.lower,request.args['events']))
	
	events = ['exam', 'duty']
	number = 6313577459
	event_dates = get_event_dates(events, creds) 
	
	for event in event_dates:
		event_name = event[0]
		event_date = event[1]

		event_date_object = datetime.strptime(event_date, '%Y-%m-%dT%H:%M:%S-%f:00') 
		run_date = event_date_object - timedelta(minutes=30)
		id_ = event_date+str(number)
		msg_body = "You have %s in 30 minutes" % (event_name)
		
		#if the job does not exist run it
		if not app.apscheduler.get_job(id=id_):
			app.apscheduler.add_job(func=send_text_notification, trigger='date', args=[str(number), msg_body], id=id_, run_date=run_date)
		
			print("Created a scheduled job for the number {} for the event {}".format(number, msg_body))

	if app.apscheduler.get_jobs():
		print('Finished creating jobs')
	
	return 'Finished scheduling events'

@app.route('/schedule_duty',methods=['POST'])
def schedule_duty():
	filename = start_schedule(json.loads(request.data))
	return send_from_directory(app.config['EXCEL_FILES'], filename, as_attachment=True)

@app.route('/add_duty_to_caledar')
def add_duty_to_calendar():
	duty_dates = get_duty_dates_from_sheet('Pharez', '2020 RA Duty')
	creds = request.cookies
	add_events(duty_dates, creds, 'Duty', 20, 0)
	return 'Event Created '

#not currently working
def remove_event(event_date, number):
	app.scheduler.remove_job(id=event_date+str(number))

if __name__ == "__main__":
	#main()
	app.run(host='localhost', debug=True, port=8000)
	#https = ssl_context='adhoc'
	#schedule_events(54)
	#time.sleep(1455)
