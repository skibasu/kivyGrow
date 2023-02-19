from datetime import date, datetime, time, timedelta


class ConfigApp:

    def __init__(self, start, period):
        self.start = start
        self.is_running = False
        #self.isStarted = False

        self.set_period(period)
        self.set_end_time()

    def toggle_app(self):
        if self.is_running:
            self.is_running = False
        else:
            self.is_running = True

    def get_is_Running(self):
        return self.is_running

    def set_end_time(self):
        t = datetime.combine(date.today(), time(
            self.start['hour'], self.start['minute'])) + timedelta(minutes=1)
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