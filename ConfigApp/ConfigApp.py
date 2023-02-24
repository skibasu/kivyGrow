from datetime import date, datetime, time, timedelta
from api.api import Api

api = Api()


class ConfigApp:

    def __init__(self):
        config = api.get_config()

        self.start = config["start"]
        self.end = config["end"]
        self.is_running = config["is_running"]
        self.period = config["period"]
        self.humidity_ranges = config["humidity_ranges"]
        self.started_at = config["started_at"]
        self.current_day = config["current_day"]
        self.current_v_day = config["current_v_day"]
        self.current_f_day = config["current_f_day"]

    def start_is_running(self):
        self.is_running = True
        api.update_config({"is_running": True})

    def get_is_running(self):
        return self.is_running

    def set_start_time(self, start):
        self.start = start
        api.update_config({"start": self.start})

    def set_end_time(self):
        if (self.period != 0):
            t = datetime.combine(date.today(), time(
                self.start['hour'], self.start['minute'])) + timedelta(hours=self.period)
            self.end = {"hour": int(t.strftime('%H')),
                        "minute": int(t.strftime('%M'))}
        api.update_config({"end": self.end})

    def set_period(self, value):

        if value == "vegetative":
            self.period = 18
        elif value == "flowering":
            self.period = 12
        api.update_config({"period": value})

    def get_period(self):
        return self.period

    def get_range(self):
        return [self.start, self.end]

    def set_ranges_of_humidity(self, ranges):
        self.humidity_ranges = ranges
        api.update_config({"humidity_ranges": ranges})

    def get_ranges_of_humidity(self):
        return self.humidity_ranges

    def set_current_day(self, day):
        self.current_day = day

    def get_current_day(self):
        return self.current_day

    def get_current_f_day(self):
        return self.current_f_day

    def set_current_f_day(self, day):
        self.current_f_day = day

    def get_current_v_day(self):
        return self.current_v_day

    def set_current_v_day(self, day):
        self.current_v_day = day

    def get_started_at(self):
        return self.started_at

    def set_started_at(self):
        self.started_at = datetime.now()
