import os
import time
import calendar
from datetime import datetime
from pprint import pprint
from collections import defaultdict
from excel_calendar import create_excel_calendar, write_to_excelsheet, get_duty_dates_from_sheet

current_index = {'weekends': 0, 'weekdays':0}
total_days = {'weekends': 0, 'weekdays': 0}
NO_ASSIGNMENT = 'unable to assign'


class Scheduler:

    def __init__(self, payload):
        self.start_date = datetime.strptime(payload['startDate'], '%Y-%m-%d')
        self.end_date = datetime.strptime(payload['endDate'], '%Y-%m-%d')
        self.year = self.start_date.year
        self.months = [str(x) for x in range(self.start_date.month, self.end_date.month + 1)]
        self.filename = '2020 {} Duty'.format(payload['hall'])
        self.doubleDuty = payload['doubleDuty']
        self.duty_dates = defaultdict(dict)
        self.staff = [staff_member['name'] for staff_member in payload['staffData'] ] + [NO_ASSIGNMENT]
        
        self.preferences = {staff_member['name']: {month:[] for month in self.months} for staff_member in payload['staffData']}

        for person in payload['staffData']:
            for prefDayOff in person['preferences']:
                if prefDayOff:
                    date_obj = datetime.strptime(prefDayOff, '%Y-%m-%d')
                    self.preferences[person['name']][str(date_obj.month)].append(date_obj.day)

    # ---------Algorithm functions--------------------
    def assign_RD_to_block ():
        pass
        
    def assign_ra_to_day(self, day, month, day_type):
        staff_names = list(self.preferences.keys())
        current_RA_index = None
        RA = staff_names[current_index[day_type]]
        mod = len(self.preferences)

        next_available_RA_index = (current_index[day_type] + 1) % mod
        current_RA_index = current_index[day_type]
        
        if current_index[day_type] == 0:
            total_days[day_type] += 1

        #-----------------Algorithm----------------------------------------
        #This algo assigns an RA
        while (day in self.preferences[RA][month]                       or 
               self.duty_dates[RA][day_type] >= total_days[day_type]    or 
               day in self.duty_dates[RA][month]
               ):
      
            RA = staff_names[next_available_RA_index]
            next_available_RA_index += 1
            next_available_RA_index %= mod
            
            # Handles edge case where we attempt to even out the days but can't since someone can't sit
            # a certain day
            if next_available_RA_index == current_RA_index:
                starting_RA_index = next_available_RA_index
                while day in self.preferences[RA][month]:
                    RA = staff_names[next_available_RA_index]
                    next_available_RA_index += 1
                    next_available_RA_index %= mod

                    #this control handles edge where no one can sit a day
                    if next_available_RA_index == starting_RA_index:
                        RA = NO_ASSIGNMENT
                        break 
                break

        current_index[day_type] += 1
        if current_index[day_type] == len(self.preferences):
            current_index[day_type] = 0

        return RA

    def assign_dates_by_month(self):
        day_types = ['weekdays', 'weekends']
        
        for month in self.months:
            weekdays, weekends = self.create_calendar(month)
            self.add_month_to_duty_dates(month)

            for day in weekdays:
                RA = self.assign_ra_to_day(day, month, 'weekdays')
                self.duty_dates[RA][month].append(day)
                self.duty_dates[RA]['weekdays'] += 1

            for day in weekends:
                RA = self.assign_ra_to_day(day, month, 'weekends')
                self.duty_dates[RA][month].append(day)
                self.duty_dates[RA]['weekends'] += 1

                if self.doubleDuty:
                    RA = self.assign_ra_to_day(day, month, 'weekends')
                    self.duty_dates[RA][month].append(day)
                    self.duty_dates[RA]['weekends'] += 1

        #print_duty_dates(duty_dates)

    def create_calendar(self, month):
        c = calendar.TextCalendar(calendar.SUNDAY)
        weekdays = []
        weekends = []
        month_int = int(month)

        for day in c.itermonthdays2(self.year, month_int):
            
            if [month_int, day[0]] == [self.end_date.month, self.end_date.day + 1]:
                break
            
            if day[0] != 0:
                if month_int != self.start_date.month or day[0] >= self.start_date.day:
                    if day[1] in [4, 5]:
                        weekends.append(day[0])
                    else:
                        weekdays.append(day[0])

        return weekdays, weekends

    def add_month_to_duty_dates(self, month):
        for ra in self.staff:
            self.duty_dates[ra][month] = []
            if 'weekdays' not in self.duty_dates[ra]:
                self.duty_dates[ra]['weekdays'] = 0
                self.duty_dates[ra]['weekends'] = 0

    #----- Sorts duty dates by month -----
    def decompose_duty_dates(self):
        duty_dates_by_month = defaultdict(dict)
        total_duty_dates = defaultdict(dict)
        for month in self.months:
            for name in self.duty_dates:
                for day in self.duty_dates[name][month]:
                    if day in duty_dates_by_month[month]:
                        duty_dates_by_month[month][day] += " and %s" %(name)
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

        cleanup = True
        if cleanup:
            if os.path.exists(self.filename + ".xlsx"):
                os.remove(self.filename + ".xlsx")
        
        self.assign_dates_by_month()
        self.duty_dates, total_days = self.decompose_duty_dates()
        write_to_excelsheet(self.duty_dates, total_days, self.months, self.year, self.filename)
        
        #os.startfile('%s.xlsx' % self.filename)

    '''
        preferences = {'Anya': {'8':[5, 12, 19, 26], '9':[], '10':[], '11':[]}, 
                       'Chris': {'8':[], '9':[], '10':[], '11':[]}, 
                       'Chelsea': {'8':[], '9':[], '10':[], '11':[]}, 
                       'Nate': {'8':[], '9':[], '10':[], '11':[]},
                       'Veronica': {'8':[], '9':[], '10':[6, 13, 20, 27], '11':[]},
                       'Juan': {'8':[], '9':[], '10':[], '11':[]}
                       }

    #I want to refactor my code and shy away from using ints and using dateimte objects.
    #This will improve readability

    '''

