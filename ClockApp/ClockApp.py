from datetime import datetime, time


class Clock:

    def __init__(self, config, others):

        self.config = config
        self.time_clock = "0:00"
        self.calendar = ""
        self.led_lamp = others["led_lamp"]
        self.time_of_the_day = others["time_of_the_day"]

        self.set_time()

    def set_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%A, %d, %B, %Y")

        if (current_time != self.get_time()):
            self.time_clock = current_time

        if (current_date != self.get_calendar()):
            self.calendar = current_date

    def check_range(self):

        start_h = self.config["get_range"]()[0]["hour"]
        start_m = self.config["get_range"]()[0]["minute"]
        end_h = self.config["get_range"]()[1]["hour"]
        end_m = self.config["get_range"]()[1]["minute"]

        self.time_in_range(time(start_h, start_m), time(
            end_h, end_m), datetime.now().time())

    def get_time(self):
        return self.time_clock

    def get_calendar(self):
        return self.calendar

    def set_sunny_day(self):
        self.led_lamp.on()
        self.time_of_the_day.set_status("day")

    def set_dark_night(self):
        self.led_lamp.off()
        self.time_of_the_day.set_status("night")

    def time_in_range(self, start, end, current):

        # during two days
        if (start >= end):
            if (current >= start or current <= end):
                if (self.led_lamp.get_status() == False):
                    self.set_sunny_day()
            else:
                if (self.led_lamp.get_status() == True):
                    self.set_dark_night()

        # during one day
        if (start <= end):
            if (current >= start and current <= end):
                if (self.led_lamp.get_status() == False):
                    self.set_sunny_day()
            else:
                if (self.led_lamp.get_status() == True):
                    self.set_dark_night()
