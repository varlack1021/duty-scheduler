import os
import xlrd
import time
import calendar
from openpyxl import load_workbook
from datetime import datetime
from collections import defaultdict
from excel_calendar import create_excel_calendar

# are lists objects?
# list of dates we do not  want to sit

# need to pick dates, could do this randomly -Done
# need to keep track of how many dates everyone has sat. -Done
# This could be a text file
# Output, a list of dates? -Done
# Should we consider dates people
# List of prefernces should switch to months
# consider weekends equaility -
# consider weekdays equality
# The way this is done needs to be fixed
# SRAS sit two weekendss a month
# Check if the SRA was already scheduled for the week, I can check 
# Improvements? Well what does it currently do? It currently has days we can't sit, evens out days
# Does not remember previous number of days. Can it be stored in a cookie?
# Add support for double duty weekend
'''
Issues
Program wont work if everyone decides not to sit on one day.
Does not have SRA sit on one day
name casing
google refresh tokens
'''
current_index = {'weekends': 0, 'weekdays':0}
total_days = {'weekends': 0, 'weekdays': 0}

def assign_ra_to_day(day, month, preferences, duty_dates, day_type):
    current_RA_index = None

    RA = list(preferences.keys())[current_index[day_type]]
    next_available_RA_index = current_index[day_type] + 1
    current_RA_index = current_index[day_type]
    
    if current_index[day_type] == 0:
        total_days[day_type] += 1

    #-----------------Algorithm----------------------------------------
    while day in preferences[RA][str(month)] or duty_dates[RA][day_type] >= total_days[day_type]:

        if next_available_RA_index == len(preferences.keys()):
            next_available_RA_index = 0

        RA = list(preferences.keys())[next_available_RA_index]
        next_available_RA_index += 1

        # Handles edge case where we attempt to even out the days but can't since someone can't sit
        # a certain day
        if next_available_RA_index == current_RA_index:
            while day in preferences[RA]:
                if next_available_RA_index == len(preferences.keys()):
                    next_available_RA_index = 0   
                
                RA = list(preferences.keys())[next_available_RA_index]
                next_available_RA_index += 1
            
            break

    current_index[day_type] += 1
    if current_index[day_type] == len(preferences):
        current_index[day_type] = 0

    return RA

def create_calendar(year, month_int, start_date):
    c = calendar.TextCalendar(calendar.SUNDAY)
    weekdays = []
    weekends = []
    
    for day in c.itermonthdays2(year, month_int):
        if day[0] != 0:
            if month_int != start_date[0] or day[0] >= start_date[1]:
                if day[1] in [5, 6]:
                    weekends.append(day[0])
                else:
                    weekdays.append(day[0])

    return weekdays, weekends

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

def assign_dates_by_month(staff, preferences, months, start_date, year):
    duty_dates = defaultdict(dict)
    day_types = ['weekdays', 'weekends']
    
    for month in months:
        weekdays, weekends = create_calendar(year, month, start_date)
        duty_dates = add_month_to_duty_dates(duty_dates, staff, month)
        print(weekdays, weekends)

        for day in weekdays:
            RA = assign_ra_to_day(day, month, preferences, duty_dates, 'weekdays')
            duty_dates[RA][month].append(day)
            duty_dates[RA]['weekdays'] += 1

        for day in weekends:
            RA = assign_ra_to_day(day, month, preferences, duty_dates, 'weekends')
            duty_dates[RA][month].append(day)
            duty_dates[RA]['weekends'] += 1

    print_duty_dates(duty_dates)
    return duty_dates

def add_month_to_duty_dates(duty_dates, staff, month):
    for ra in staff:
        duty_dates[ra][month] = []
        if 'weekdays' not in duty_dates[ra]:
            duty_dates[ra]['weekdays'] = 0
            duty_dates[ra]['weekends'] = 0

    return duty_dates

def duty_dates_to_month_dic(duty_dates, months):
    duty_dates_by_month = defaultdict(dict)
    for month in months:
        for name in duty_dates:
            for day in duty_dates[name][month]:
                duty_dates_by_month[month][day] = name
    
    return duty_dates_by_month

def write_to_excelsheet(duty_dates, months, year, filename):
    '''
    The algorithm iterates through the cells in the excel sheet that have a date.
    The algo checks if the date is inlcuded in scheduled duty dates
    '''
    create_excel_calendar(year, filename)
    loc = '%s.xlsx' % (filename)
    #wb = xlrd.open_workbook(loc)

    write_wb = load_workbook(loc)
    read_wb = xlrd.open_workbook(loc)

    for month_number in months:
        datetime_object = datetime.strptime(str(month_number), "%m")
        month_name = datetime_object.strftime('%B')
        write_sheet = write_wb[month_name]
        read_sheet = read_wb.sheet_by_name(month_name)

        for row in range(2, write_sheet.max_row, 2):
            
            for col in range(write_sheet.max_column):
                day = read_sheet.cell_value(row, col)
                if day in duty_dates[month_number].keys() and day:
                    row_num = row + 1
                    name = duty_dates[month_number][day]
                    cell = write_sheet.cell(row_num + 1, col + 1)
                    cell.value = name

        write_wb.save(loc)

def get_duty_dates_from_sheet(name, filename):
    filename = '%s.xlsx' % (filename)
    duty_dates = {}
    wb = xlrd.open_workbook(filename)
    
    for sheet in wb.sheets():

        if any(sheet.row_values(5)):
            month_number = list(calendar.month_name).index(sheet.name)
            duty_dates[month_number] = []
            
            for row in range(2, sheet.nrows):

                row_values = sheet.row_values(row)
                if name in row_values:
                    columns = [i for i, x in enumerate(row_values) if x == name]
                    days = [sheet.cell(row-1, x).value for x in columns]
                    duty_dates[month_number].extend(days)
    
    if duty_dates[list(duty_dates.keys())[0]][0] > 31:        
        duty_dates = convert_excel_date(duty_dates)

    return duty_dates

def convert_excel_date(duty_dates):
    for month, excel_day in duty_dates.items():
        print(duty_dates)
        days = [xlrd.xldate_as_tuple(day, 0)[2] for day in excel_day]
        duty_dates[month] = days
    print(duty_dates)
    return duty_dates

def start_schedule():
    year = 2020
    start_date = [9, 7]
    months = [10]
    staff = ['Anya', 'Chris', 'Chelsea', 'Nate', 'Veronica', 'Juan']
    
    preferences = {'Anya': {'8':[5, 12, 19, 26], '9':[], '10':[], '11':[]}, 
                   'Chris': {'8':[], '9':[], '10':[], '11':[]}, 
                   'Chelsea': {'8':[], '9':[], '10':[], '11':[]}, 
                   'Nate': {'8':[], '9':[], '10':[], '11':[]},
                   'Veronica': {'8':[], '9':[], '10':[6, 13, 20, 27], '11':[]},
                   'Juan': {'8':[], '9':[], '10':[], '11':[]}
                   }
    
    duty_dates = assign_dates_by_month(staff, preferences, months, start_date, year)
    duty_dates = duty_dates_to_month_dic(duty_dates, months)
    write_to_excelsheet(duty_dates, months, year, '2020 RA Duty')
    os.startfile('2020 RA Duty.xlsx')

#get_duty_dates_from_sheet('Pharez', '2020 RA Duty')
#start_schedule()

'''
I need to design a frontend, once thats done deploy!
Add a param for staff types
'''
