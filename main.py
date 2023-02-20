from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from ConfigApp.ConfigApp import ConfigApp
from ClockApp.ClockApp import Clock as ClockApp
from LedLamp.LedLamp import LedLamp
from kivy.clock import Clock as BackgroundClock
from TimeOfTheDay.TimeOfTheDay import TimeOfTheDay
from Weather.Weather import Weather
from datetime import time

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "600")

app_config = ConfigApp({"hour": 7, "minute": 0}, "vegetative")
led_lamp = LedLamp()
time_of_the_day = TimeOfTheDay()
weather = Weather()
clock = ClockApp({"get_range": app_config.get_range}, {
    "led_lamp": led_lamp, "time_of_the_day": time_of_the_day})


class MyWidget(BoxLayout):

    def __init__(self, **kwargs):

        super(MyWidget, self).__init__(**kwargs)

    def set_time(self, args=None):
        self.ids.clock.text = clock.get_time()

    def update_clock(self, args=None):
        clock.set_time()
        self.set_time()
        self.update_day_icon()

    def update_weather(self, args=None):
        temperature = weather.get_temp_hum()[0]
        temperature_str = str(temperature)
        humidity = weather.get_temp_hum()[1]
        humidity_str = str(humidity)
        weather.check_temp_and_humidity()

        if (self.ids.temperature.text != temperature_str):
            self.ids.temperature.text = temperature_str+"\N{DEGREE SIGN}C"
            self.ids.temperature.progress = -140 + \
                temperature * 5.6
            self.set_temp_colors(temperature)

        if (self.ids.humidity.text != humidity_str):
            self.ids.humidity.text = humidity_str+"%"
            self.ids.humidity.progress = -140 + humidity * 2.8
            self.set_hum_colors(humidity)

    def set_temp_colors(self, temp):
        is_lamp_on = led_lamp.get_status()

        if is_lamp_on:
            if temp > 0 and temp < 18:
                self.ids.temperature.progress_color = (
                    62 / 253, 12 / 253, 229 / 253, 1)
            elif temp >= 18 and temp <= 28:
                self.ids.temperature.progress_color = (
                    229 / 253, 146 / 253, 12 / 253, 1)
            elif temp > 28 and temp < 32:
                self.ids.temperature.progress_color = (
                    255 / 253, 80 / 253, 80 / 253, 1)
            elif temp >= 32:
                self.ids.temperature.progress_color = (
                    209 / 253, 8 / 253, 8 / 253, 1)

        else:
            if temp < 16:
                self.ids.temperature.progress_color = (
                    62 / 253, 12 / 253, 229 / 253, 1)
            if temp >= 16 and temp < 22:
                self.ids.temperature.progress_color = (
                    229 / 253, 146 / 253, 12 / 253, 1)
            elif temp >= 22 and temp < 25:
                self.ids.temperature.progress_color = (
                    255 / 253, 80 / 253, 80 / 253, 1)
            elif temp >= 25:
                self.ids.temperature.progress_color = (
                    209 / 253, 8 / 253, 8 / 253, 1)

    def set_hum_colors(self, hum):
        period = app_config.get_period()

        if period == 18:
            if hum > 0 and hum < 50:
                self.ids.humidity.progress_color = (
                    229 / 253, 179 / 253, 12 / 253, 1)
            elif hum >= 50 and hum < 65:
                self.ids.humidity.progress_color = (
                    12 / 253, 187 / 253, 229 / 253, 1)
            elif hum >= 65 and hum > 80:
                self.ids.humidity.progress_color = (
                    32 / 253, 87 / 253, 211 / 253, 1)
            elif hum >= 80:
                self.ids.humidity.progress_color = (
                    11 / 253, 50 / 253, 137 / 253, 1)

        elif period == 12:
            if hum > 0 and hum < 30:
                self.ids.humidity.progress_color = (
                    229 / 253, 179 / 253, 12 / 253, 1)
            elif hum >= 30 and hum < 40:
                self.ids.humidity.progress_color = (
                    12 / 253, 187 / 253, 229 / 253, 1)
            elif hum >= 40 and hum > 50:
                self.ids.humidity.progress_color = (
                    32 / 253, 87 / 253, 211 / 253, 1)
            elif hum >= 50:
                self.ids.humidity.progress_color = (
                    11 / 253, 50 / 253, 137 / 253, 1)

    def set_calendar(self):

        self.ids.calendar.text = clock.get_calendar()

    def toggle_day_icon(self):
        self.time_of_the_day_source = time_of_the_day.get_icon()

    def update_day_icon(self):
        if (time_of_the_day.get_icon() != self.time_of_the_day_source):
            self.time_of_the_day_source = time_of_the_day.get_icon()

    def initialize_day_time(self):
        if (led_lamp.get_status() == 1):
            time_of_the_day.set_status('day')

        elif (led_lamp.get_status() == 0):
            time_of_the_day.set_status('night')

        self.time_of_the_day_source = time_of_the_day.get_icon()

    def initialize_start_end(self):
        range = app_config.get_range()
        start = range[0]
        end = range[1]

        self.ids.day_start.text = "DAY STARTS AT " + \
            time(start["hour"], start["minute"]).strftime("%H:%M")
        self.ids.day_end.text = "DAY FINISHES AT " + \
            time(end["hour"], end["minute"]).strftime("%H:%M")

    def toggle_start(self):
        app_config.toggle_app()
        is_runnig = app_config.get_is_Running()

        if (is_runnig):
            self.ids.start_btn.text = "END GROW"
            self.ids.start_btn.background_color = [
                199 / 253, 68 / 253, 73 / 253, 1]

        else:
            self.ids.start_btn.text = "START GROW"
            self.ids.start_btn.background_color = [
                73 / 253, 106 / 253, 72 / 253, 1]


class GrowboxApp(App):

    def build(self):
        widget = MyWidget()
        widget.initialize_start_end()
        widget.set_time()
        widget.set_calendar()
        widget.initialize_day_time()

        BackgroundClock.schedule_interval(widget.update_clock, 1)
        BackgroundClock.schedule_interval(widget.update_weather, 3)

        return widget


if __name__ == '__main__':
    GrowboxApp().run()
