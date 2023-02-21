from datetime import date, datetime, time, timedelta


class ConfigApp:

    def __init__(self):
        self.start = ""
        self.end = ""
        self.is_running = False
        self.period = None
        self.humidity_ranges = {
            "vegetative": {
                "humidity_min": "60",
                "humidity_max": "80"
            },
            "flowering": {
                "humidity_min": "45",
                "humidity_max": "55"
            }
        }

    def toggle_app(self):
        if self.is_running:
            self.is_running = False
        else:
            self.is_running = True

    def start_is_running(self):
        self.is_running = True

    def get_is_running(self):
        return self.is_running

    def set_start_time(self, start):
        self.start = start

    def set_end_time(self):
        if (self.period != None):
            t = datetime.combine(date.today(), time(
                self.start['hour'], self.start['minute'])) + timedelta(hours=self.period)
            self.end = {"hour": int(t.strftime('%H')),
                        "minute": int(t.strftime('%M'))}

    def set_period(self, value):

        if value == "vegetative":
            self.period = 18
        elif value == "flowering":
            self.period = 12

    def get_period(self):
        return self.period

    def get_range(self):
        return [self.start, self.end]

    def set_ranges_of_humidity(self, ranges):
        self.humidity_ranges = ranges

    def get_ranges_of_humidity(self):
        return self.humidity_ranges
