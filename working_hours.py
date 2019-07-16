from datetime import datetime as dt
from datetime import timedelta

FMT = "%H:%M"
PARSE = (f"00:00", FMT)
DEFAULT_DICT = {
    "Monday": {"start": "0000", "end": "0000"},
    "Tuesday": {"start": "0000", "end": "0000"},
    "Wednesday": {"start": "0000", "end": "0000"},
    "Thursday": {"start": "0000", "end": "0000"},
    "Friday": {"start": "0000", "end": "0000"},
    "Saturday": {"start": "0000", "end": "0000"},
    "Sunday": {"start": "0000", "end": "0000"},
}


class WorkingTime:
    def __init__(self, worker, company, num_hours_to_work, days_dict=None):
        self.worker = worker
        self.company = company
        self.num_hours_to_work = self.parse_hours(num_hours_to_work)
        # This can be a JSON file or a SQL DB
        self.days_dict = days_dict or DEFAULT_DICT

    def parse_hours(self, num_hours_to_work):
        p = str(num_hours_to_work) + "0" * (4 - (len(str(num_hours_to_work))))
        h, m = f"{p[:2]}:{p[2:4]}".split(":")
        return timedelta(hours=int(h), minutes=int(m))

    def fmt_day(self, day):
        return day.title()

    def set_start_hour(self, day, hour):
        self.days_dict[self.fmt_day(day)]["start"] = hour
        return self

    def set_end_hour(self, day, hour):
        self.days_dict[self.fmt_day(day)]["end"] = hour
        return self

    def set_start_and_end(self, day, start, end):
        self.set_start_hour(day, start)
        self.set_end_hour(day, end)
        return self

    def get_start_hour(self, day):
        return self.days_dict[self.fmt_day(day)]["start"]

    def get_end_hour(self, day):
        return self.days_dict[self.fmt_day(day)]["end"]

    def get_start_and_end(self, day):
        return self.get_start_hour(day), self.get_end_hour(day)

    def parse_datetime(self, hour):
        return dt.strptime(f"{hour[:2]}:{hour[2:4]}", FMT)

    def calculate_day_hours(self, hours):
        """ takes in a tuple and returns the number of hours"""
        start, end = hours
        try:
            start_time_obj = self.parse_datetime(start)
            end_time_obj = self.parse_datetime(end)
            return (end_time_obj - start_time_obj).total_seconds() / 3600
        except ValueError:
            return dt.strptime(*PARSE).strftime(FMT)

    def calculate_week_hours(self):
        """ returns the sum of the week """
        total = 0.0
        for k, v in self.days_dict.items():
            if v.get("start") and v.get("end"):
                hours = self.calculate_day_hours((v.get("start"), v.get("end")))
                total += hours
        return total

    def hours_remaining(self):
        """ Returns the hours left to work in the week"""
        return (
            self.num_hours_to_work.total_seconds() / 3600
        ) - self.calculate_week_hours()

    def display_hours_day(self, day, hours):
        """ Returns a string of the hours for that day """
        day_hours = self.get_start_and_end(day)
        rtn_hours = self.calculate_day_hours(day_hours)
        space = " " * (11 - len(day))
        return f"\n\t{self.fmt_day(day)}{space}::  {rtn_hours} Hours\n"

    def display_hours_week(self):
        """ Returns a string of the hours for the week and the hours remaining"""
        rtn_str = "\n"
        rtn_str += f"\n\tName       ::  {self.worker}\n\tCompany    ::  {self.company}"
        line = "-" * 50
        total_line = "-" * 26
        rtn_str += f"\n{line}"
        for k, v in self.days_dict.items():
            if v:
                hours = self.calculate_day_hours((v.get("start"), v.get("end")))
                rtn_str += self.display_hours_day(k, hours)
        total = self.calculate_week_hours()
        rtn_str += f"\t{total_line}"
        rtn_str += f"\n\tTotal      ::  {total} Hours\n"
        rtn_str += f"\t{total_line}"
        rtn_str += f"\n\tRemain     ::  {self.hours_remaining()} Hours\n"
        rtn_str += f"\n{line}\n\n"

        return rtn_str


if __name__ == "__main__":
    # init and set hours
    wt = (
        WorkingTime("Maffaz", "IT Circle Consult", 40)
        .set_start_hour("monday", "0730")
        .set_end_hour("monday", "1800")
        .set_start_and_end("TUESDAY", "0730", "1800")
        .set_start_and_end("wednesday", "0000", "0000")
        .set_start_and_end("THUrsday", "0000", "0000")
        .set_start_and_end("FrIDAY", "0000", "0000")
    )

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

    # print week hours total and remaining hours
    print(wt.display_hours_week())
