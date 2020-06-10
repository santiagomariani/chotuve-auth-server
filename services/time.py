from datetime import datetime, timedelta
import os

class Time():

    def get_date(self):
        return datetime.utcnow()
    
    def sum_minutes_to_date(self, date, minutes):
        return date + timedelta(minutes=minutes)


class TimeFake():

    def __init__(self):
        self.date = datetime.utcnow()

    def set_date(self, a_date):
        self.date = a_date

    def get_date(self):
        return self.date

    def sum_minutes_to_date(self, date, minutes):
        return date + timedelta(minutes=minutes)

time_service = Time() if os.environ['APP_SETTINGS'] != 'testing' else TimeFake()