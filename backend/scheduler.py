import os
import time
import calendar
import pandas as pd
import datetime as dt
from collections import defaultdict
from excel_calendar import Excel_Calendar

current_index = {'weekends': 0, 'weekdays':0}
total_days = {'weekends': 0, 'weekdays': 0}
NO_ASSIGNMENT = 'unable to assign'


class Scheduler:

    def __init__(self, payload):
        self.start_date = dt.datetime.strptime(payload['startDate'], '%Y-%m-%d')
        self.end_date = dt.datetime.strptime(payload['endDate'], '%Y-%m-%d')
        self.month_range = set(dt.date(date.year, date.month, 1) for date in pd.date_range(self.start_date, self.end_date))
        self.filename = '2020 {} Duty'.format(payload['hall'])
        self.doubleDuty = payload['doubleDuty']
        self.duty_dates = defaultdict(dict)
        self.staff = [staff_member['name'] for staff_member in payload['staffData'] ] + [NO_ASSIGNMENT]
        self.preferences = {staff_member['name']: staff_member['preferences'] for staff_member in payload['staffData']}
        self.duty_type = payload.get('duty_type')

    # ---------Algorithm functions--------------------  
    def assign_staff_member_to_day(self, date, day_type):
        staff_names = list(self.preferences.keys())
        current_RA_index = None
        RA = staff_names[current_index[day_type]]
        mod = len(self.preferences)

        date_obj = dt.datetime.strptime(date, '%Y-%m-%d')
        month = date_obj.month
        day = date_obj.day
        
        next_available_RA_index = (current_index[day_type] + 1) % mod
        current_RA_index = current_index[day_type]
        
        if current_index[day_type] == 0:
            total_days[day_type] += 1

        #-----------------Algorithm----------------------------------------
        #This algo assigns an RA
        while (date in self.preferences[RA]                             or 
               self.duty_dates[RA][day_type] >= total_days[day_type]    
               ):
      
            RA = staff_names[next_available_RA_index]
            next_available_RA_index += 1
            next_available_RA_index %= mod
            
            # Handles edge case where we attempt to even out the days but can't since someone can't sit
            # a certain day
            if next_available_RA_index == current_RA_index:
                starting_RA_index = next_available_RA_index
                while date in self.preferences[RA]:
                    RA = staff_names[next_available_RA_index]
                    next_available_RA_index += 1
                    next_available_RA_index %= mod

                    #this control handles edge where no one can sit a day
                    if next_available_RA_index == starting_RA_index:
                        RA = NO_ASSIGNMENT
                        break 
                break

        current_index[day_type] += 1
        current_index[day_type] %= mod

        return RA

    def assign_ra_by_month(self):        
        for date in self.month_range:
            weekdays, weekends = self.create_calendar(date)
            self.add_month_to_duty_dates(date)
            month = date.month

            for day in weekdays:
                dt = "{}-{:02d}-{:02d}".format(date.year, date.month, day)
                RA = self.assign_staff_member_to_day(dt, 'weekdays')
                self.duty_dates[RA][month].append(day)
                self.duty_dates[RA]['weekdays'] += 1

            for day in weekends:
                dt = "{}-{:02d}-{:02d}".format(date.year, date.month, day)
                RA = self.assign_staff_member_to_day(dt, 'weekends')
                self.duty_dates[RA][month].append(day)
                self.duty_dates[RA]['weekends'] += 1

                if self.doubleDuty:
                    RA = self.assign_staff_member_to_day(dt,'weekends')
                    self.duty_dates[RA][month].append(day)
                    self.duty_dates[RA]['weekends'] += 1

    def create_calendar(self, date):
        c = calendar.TextCalendar(calendar.SUNDAY)
        weekdays = []
        weekends = []

        for day in c.itermonthdays2(date.year, date.month):
            
            if [date.month, day[0]] == [self.end_date.month, self.end_date.day + 1]:
                break
            
            if day[0] != 0:
                if date.month != self.start_date.month or day[0] >= self.start_date.day:
                    if day[1] in [4, 5]:
                        weekends.append(day[0])
                    else:
                        weekdays.append(day[0])

        return weekdays, weekends

    def add_month_to_duty_dates(self, date):
        for ra in self.staff:
            self.duty_dates[ra][date.month] = []
            if 'weekdays' not in self.duty_dates[ra]:
                self.duty_dates[ra]['weekdays'] = 0
                self.duty_dates[ra]['weekends'] = 0

    #----- Sorts duty dates by month -----
    def decompose_duty_dates(self):
        duty_dates_by_month = defaultdict(dict)
        total_duty_dates = defaultdict(dict)
        for date in self.month_range:
            for name in self.duty_dates:
                month = date.month
                for day in self.duty_dates[name][month]:
                    if day in duty_dates_by_month[month]:
                        duty_dates_by_month[month][day] += " and %s" % (name)
                    else:
                        duty_dates_by_month[month][day] = name
                                    
                del self.duty_dates[name][month]
                total_duty_dates[name] = self.duty_dates[name]
        
        return duty_dates_by_month, total_duty_dates

    #----- Print Duty Dates---------------
    def print_duty_dates(self):
        value_iterator = iter(self.duty_dates)
        first_key = next(value_iterator)
        months = duty_dates[first_key]

        # this func ensures we only print the month keys
        for month in months:
            if type(month) is int:
                print('\n---Duty dates for month {}----\n'.format(calendar.month_name[month]))
                for RA in self.duty_dates:
                    print(RA, self.duty_dates[RA][month])
        
        print_total_duty_days()

    def print_total_duty_days(self):
        print("\n---Total Duty Days---\n")
        for RA in self.duty_dates:
            print('''{} has {} days of weekdays duty and {} days of weekends duty.'''
                .format(RA, self.duty_dates[RA]['weekdays'], self.duty_dates[RA]['weekends']))

    #---- Main function ----
    def start_schedule(self):

        cleanup = False
        if cleanup:
            if os.path.exists(self.filename + ".xlsx"):
                os.remove(self.filename + ".xlsx")

        self.assign_ra_by_month()
        self.duty_dates, total_days = self.decompose_duty_dates()
        
        excel_obj_tool = Excel_Calendar(self.filename)
        excel_obj_tool.write_to_excelsheet(self.duty_dates, total_days, self.month_range)
    
