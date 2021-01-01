import datetime
import os.path
from googleapiclient.discovery import build
import google.oauth2.credentials
import google_auth_oauthlib.flow

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.readonly']
redirect_uri = 'https://b8f551372fb5.ngrok.io/googlecallback'

#Using the google api client libary
#This handles tasks we would otherwise need to define
#Determines when the application can use refresh stored access tokens 
#Determines when the application must reacquire consent 
#Generates correct redirect URLS
#Helps to implement redirect handlers that exchange authorization codes for access tokens

#--------------------------------OAUTH2----------------------------
state = ''
def get_auth_url():
    global state
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json',
        #this is the scope
        SCOPES)
    #will need to upate the redirect uri name in the google oath form
    flow.redirect_uri = redirect_uri

    authorization_url, state = flow.authorization_url(
        access_type = 'offline',
        include_granted_scopes = 'true',
        prompt='consent')

    return authorization_url

def callback(authorization_response):                          
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(     
    'credentials.json',
    scopes=SCOPES,
    state=state)
    flow.redirect_uri = redirect_uri                 #savce redirect uri in configs or use flask url_for
    flow.fetch_token(authorization_response=authorization_response)
    data = credentials_to_dict(flow.credentials)
    return data                                             #does not need a return statement, will takeout once done testing

def credentials_to_dict(credentials):
  return {
          'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes
          } 

#-------- Call the Calendar API -------------
def get_event_dates(user_events, creds):
    credentials = google.oauth2.credentials.Credentials(**creds)
    service = build('calendar', 'v3', credentials=credentials)
    event_dates = []
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    
    events = events_result.get('items', [])
    
    if not events:
        print('No upcoming events found.')
    
    for event in events:
        event_name = event['summary'].lower()
        
        if any(event in event_name for event in user_events):
            event_start_date = event['start'].get('dateTime', event['start'].get('date'))
            event_dates.append((event_name, event_start_date))

    return event_dates

def add_events(duty_dates, creds, summary, s_time, e_time):
    credentials = google.oauth2.credentials.Credentials(**creds)
    service = build('calendar', 'v3', credentials=credentials)
    today = datetime.datetime.now()
   

    for month, days in duty_dates.items():
        days = list(map(int, days))
        
        for day in days:
            
            #with open('debug.txt', 'w+') as file:
                #file.write('{} {} {}'.format(day, start, month))
            
            one_day = datetime.timedelta(days=1)
            
            start = datetime.datetime(today.year, month, day, s_time)
            end =  datetime.datetime(today.year, month, day, e_time)
            end = (end + one_day)

            if 'Night' in summary:
                start = (start + one_day)

            start = start.isoformat()
            end = end.isoformat()

            body = { 'end': {'dateTime': end, 'timeZone': 'America/New_York'}, 
                     'start': {'dateTime': start, 'timeZone': 'America/New_York'}, 
                     'summary': summary
                    }
            
            service.events().insert(calendarId='primary', body=body).execute()
