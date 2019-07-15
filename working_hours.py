from datetime import datetime as dt

FMT = "%H:%M"
PARSE = (f"00:00", FMT)

class WorkingTime:
    def __init__(self, worker, company):
        self.worker = worker
        self.company = company
        # This can be a JSON file or a SQL DB
        self.days_dict = {
            "Monday": {"start": "", "end": ""},
            "Tuesday": {"start": "", "end": ""},
            "Wednesday": {"start": "", "end": ""},
            "Thursday": {"start": "", "end": ""},
            "Friday": {"start": "", "end": ""},
            "Saturday": {"start": "", "end": ""},
            "Sunday": {"start": "", "end": ""},
        }

    def set_start_hour(self, day, hour):
        self.days_dict[day.title()]["start"] = hour

    def set_end_hour(self, day, hour):
        self.days_dict[day.title()]["end"] = hour

    def set_start_and_end(self, day, start, end):
        self.days_dict[day.title()]["start"] = start
        self.days_dict[day.title()]["end"] = end

    def get_start_hour(self, day):
        return self.days_dict[day.title()]["start"]

    def get_end_hour(self, day):
        return self.days_dict[day.title()]["end"]

    def get_start_and_end(self, day):
        return self.days_dict[day.title()]["start"], self.days_dict[day.title()]["end"]

    def calculate_day_hours(self, hours):
        """ takes in a tuple and returns the number of hours"""
        start, end = hours
        try:
            start_time_obj = dt.strptime(f"{start[:2]}:{start[2:4]}", FMT)
            end_time_obj = dt.strptime(f"{end[:2]}:{end[2:4]}", FMT)
            return end_time_obj - start_time_obj
        except ValueError:
            return dt.strptime(*PARSE).strftime(FMT)

    def calculate_week_hours(self):
        """ returns the sum of the week """
        total = dt.strptime(*PARSE)
        for k, v in self.days_dict.items():
            if v.get("start") and v.get("end"):
                hours = self.calculate_day_hours((v.get("start"), v.get("end")))
                total += hours
        return total.strftime(FMT)

    def display_hours_day(self, day, hours):
        """ Returns a string of the hours for that day """
        day_hours = self.get_start_and_end(day)
        rtn_hours = self.calculate_day_hours(day_hours)
        space = " " * (11 - len(day))
        return f"\n\t{day.title()}{space}::  {rtn_hours} Hours\n"

    def display_hours_week(self):
        """ Returns a string of the hours for the week """
        rtn_str = "\n"
        rtn_str += f"\n\tName       ::  {self.worker}\n\tCompany    ::  {self.company}"
        line = "-" * 100
        rtn_str += f"\n{line}"
        for k, v in self.days_dict.items():
            if v:
                hours = self.calculate_day_hours((v.get("start"), v.get("end")))
                rtn_str += self.display_hours_day(k, hours)
        total = self.calculate_week_hours()
        rtn_str += f"\n\tTotal  ::  {total} Hours\n"
        rtn_str += f"\n{line}\n\n"
        return rtn_str


wt = WorkingTime('Maffaz', 'IT Circle Consult')

# Set hours
wt.set_start_hour("monday", "0730")
wt.set_end_hour("monday", "1800")
wt.set_start_and_end("TUESDAY", "", "")
wt.set_start_and_end("wednesday", "", "")
wt.set_start_and_end("THUrsday", "", "")
wt.set_start_and_end("FrIDAY", "", "")

# get hours
print(wt.get_start_hour("Monday"))
print(wt.get_end_hour("Wednesday"))
print(wt.get_start_and_end("Friday"))

# calculate day hours
print(wt.calculate_day_hours(wt.get_start_and_end("monday")))

# calculate week hours
week = wt.calculate_week_hours()
print(week)

# print day hours
tues_hours = wt.get_start_and_end("tuesday")
print(wt.display_hours_day("Tuesday", tues_hours))

# print week hours total
print(wt.display_hours_week())
