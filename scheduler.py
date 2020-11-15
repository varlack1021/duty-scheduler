import os
import xlrd
import time
import calendar
from openpyxl import load_workbook
from datetime import datetime
from pprint import pprint
from collections import defaultdict
from excel_calendar import create_excel_calendar, write_to_excelsheet, get_duty_dates_from_sheet

current_index = {'weekends': 0, 'weekdays':0}
total_days = {'weekends': 0, 'weekdays': 0}
DOUBLE_DUTY = False
NO_ASSIGNMENT = 'Unable to Assign'

# ---------Algorithm functions--------------------
def assign_ra_to_day(day, month, preferences, duty_dates, day_type):
    no_asssignment_dic = preferences.pop(NO_ASSIGNMENT)
    staff_names = list(preferences.keys())

    current_RA_index = None
    RA = staff_names[current_index[day_type]]
    mod = len(preferences)

    next_available_RA_index = (current_index[day_type] + 1) % mod
    current_RA_index = current_index[day_type]
    
    if current_index[day_type] == 0:
        total_days[day_type] += 1

    #-----------------Algorithm----------------------------------------
    #This algo assigns an RA
    while (day in preferences[RA][month]                    or 
           duty_dates[RA][day_type] >= total_days[day_type] or 
           day in duty_dates[RA][month]
           ):

        RA = staff_names[next_available_RA_index]
        next_available_RA_index += 1
        next_available_RA_index %= mod
        
        # Handles edge case where we attempt to even out the days but can't since someone can't sit
        # a certain day
        if next_available_RA_index == current_RA_index:
            starting_RA_index = next_available_RA_index
            while day in preferences[RA][month]:
                RA = staff_names[next_available_RA_index]
                next_available_RA_index += 1
                next_available_RA_index %= mod

                #this control handles edge where no one can sit a day
                if next_available_RA_index == starting_RA_index:
                    RA = NO_ASSIGNMENT
                    break 
            break

    current_index[day_type] += 1
    if current_index[day_type] == len(preferences):
        current_index[day_type] = 0

    preferences[NO_ASSIGNMENT] = no_asssignment_dic
    return RA

def assign_dates_by_month(staff, preferences, months, start_date, end_date, year):
    duty_dates = defaultdict(dict)
    day_types = ['weekdays', 'weekends']
    
    for month in months:
        weekdays, weekends = create_calendar(year, month, start_date, end_date)
        duty_dates = add_month_to_duty_dates(duty_dates, staff, month)

        for day in weekdays:
            RA = assign_ra_to_day(day, month, preferences, duty_dates, 'weekdays')
            duty_dates[RA][month].append(day)
            duty_dates[RA]['weekdays'] += 1

        for day in weekends:
            RA = assign_ra_to_day(day, month, preferences, duty_dates, 'weekends')
            duty_dates[RA][month].append(day)
            duty_dates[RA]['weekends'] += 1

            if DOUBLE_DUTY:
                RA = assign_ra_to_day(day, month, preferences, duty_dates, 'weekends')
                duty_dates[RA][month].append(day)
                duty_dates[RA]['weekends'] += 1

    #print_duty_dates(duty_dates)
    return duty_dates

def create_calendar(year, month, start_date, end_date):
    c = calendar.TextCalendar(calendar.SUNDAY)
    weekdays = []
    weekends = []
    month_int = int(month)

    for day in c.itermonthdays2(year, month_int):
        
        if [month_int, day[0]] == end_date:
            break
        
        if day[0] != 0:
            if month_int != start_date[0] or day[0] >= start_date[1]:
                if day[1] in [4, 5]:
                    weekends.append(day[0])
                else:
                    weekdays.append(day[0])

    return weekdays, weekends

def add_month_to_duty_dates(duty_dates, staff, month):
    for ra in staff:
        duty_dates[ra][month] = []
        if 'weekdays' not in duty_dates[ra]:
            duty_dates[ra]['weekdays'] = 0
            duty_dates[ra]['weekends'] = 0

    return duty_dates

def convert_excel_date(duty_dates):
    for month, excel_day in duty_dates.items():
        days = [xlrd.xldate_as_tuple(day, 0)[2] for day in excel_day]
        duty_dates[month] = days
    return duty_dates

#----- Sorts duty dates by month -----
def decompose_duty_dates(duty_dates, months):
    duty_dates_by_month = defaultdict(dict)
    total_duty_dates = defaultdict(dict)
    for month in months:
        for name in duty_dates:
            for day in duty_dates[name][month]:
                if day in duty_dates_by_month[month]:
                    duty_dates_by_month[month][day] += " and %s" %(name)
                else:
                    duty_dates_by_month[month][day] = name
                                
            del duty_dates[name][month]
            total_duty_dates[name] = duty_dates[name]
    return duty_dates_by_month, total_duty_dates

#----- Print Duty Dates---------------
def print_duty_dates(duty_dates):
    value_iterator = iter(duty_dates)
    first_key = next(value_iterator)
    months = duty_dates[first_key]

    # this func ensures we only print the month keys
    for month in months:
        if type(month) is int:
            print('\n---Duty dates for month {}----\n'.format(calendar.month_name[month]))
            for RA in duty_dates:
                print(RA, duty_dates[RA][month])
    
    print_total_duty_days(duty_dates)

def print_total_duty_days(duty_dates):
    print("\n---Total Duty Days---\n")
    for RA in duty_dates:
        print('''{} has {} days of weekdays duty and {} days of weekends duty.'''
            .format(RA, duty_dates[RA]['weekdays'], duty_dates[RA]['weekends']))

#---- Main function ----
def start_schedule(payload):
    start_date = datetime.strptime(payload['startDate'], '%Y-%m-%d')
    end_date = datetime.strptime(payload['endDate'], '%Y-%m-%d')

    months = [str(x) for x in range(start_date.month, end_date.month + 1)]
    year =  start_date.year
    start_date = [start_date.month, start_date.day]
    end_date = [end_date.month, end_date.day + 1]
    filename = '2020 {} Duty'.format(payload['hall'])
    
    no_asssignment = {'name': NO_ASSIGNMENT, 'preferences': []}
    payload['staffData'].append(no_asssignment)  

    global DOUBLE_DUTY
    DOUBLE_DUTY = payload['doubleDuty']

    cleanup = True
    if cleanup:
        if os.path.exists(filename + ".xlsx"):
            os.remove(filename + ".xlsx")

    staff = [staff_member['name'] for staff_member in payload['staffData']]
    
    preferences = {staff_member['name']: {month:[] for month in months} for staff_member in payload['staffData']}

    for person in payload['staffData']:
        for prefDayOff in person['preferences']:
            if prefDayOff:
                date_obj = datetime.strptime(prefDayOff, '%Y-%m-%d')
                preferences[person['name']][str(date_obj.month)].append(date_obj.day)

    duty_dates = assign_dates_by_month(staff, preferences, months, start_date, end_date, year)
    duty_dates, total_days = decompose_duty_dates(duty_dates, months)
    write_to_excelsheet(duty_dates, total_days, months, year, filename)
    os.startfile('%s.xlsx' % filename)
    return ('%s.xlsx' % filename)

'''
    preferences = {'Anya': {'8':[5, 12, 19, 26], '9':[], '10':[], '11':[]}, 
                   'Chris': {'8':[], '9':[], '10':[], '11':[]}, 
                   'Chelsea': {'8':[], '9':[], '10':[], '11':[]}, 
                   'Nate': {'8':[], '9':[], '10':[], '11':[]},
                   'Veronica': {'8':[], '9':[], '10':[6, 13, 20, 27], '11':[]},
                   'Juan': {'8':[], '9':[], '10':[], '11':[]}
                   }
#get_duty_dates_from_sheet('Pharez', '2020 RA Duty')
#start_schedule()
#I want to refactor my code and shy away from using ints and using dateimte objects.
#This will improve readability
Add enddate
Need to be able to schedule double duty.
Check if no one can sit
Add a param for staff types
'''
#x = {'startDate': '2020-8-29', 'endDate': '2020-11-18', 'hall': 'Capen', 'staffpayload': [{'name': 'Pharez', 'preferences': ['2020-11-01', '2020-11-03']}, {'name': 'Katie', 'preferences': ['2020-11-09', '2020-11-16']}]}
#start_schedule(x)
