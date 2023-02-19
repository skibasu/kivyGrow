from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from ConfigApp.ConfigApp import ConfigApp
from ClockApp.ClockApp import Clock as ClockApp
from LedLamp.LedLamp import LedLamp
from kivy.clock import Clock as BackgroundClock
from TimeOfTheDay.TimeOfTheDay import TimeOfTheDay
from Weather.Weather import Weather

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "600")

app_config = ConfigApp({"hour": 19, "minute": 21}, "vegetative")
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
        temperature = str(weather.get_temp_hum()[0])
        humidity = str(weather.get_temp_hum()[1])
        weather.check_temp_and_humidity()

        if (self.ids.temperature.text != temperature):
            self.ids.temperature.text = temperature+"\N{DEGREE SIGN}C"
        if (self.ids.humidity.text != humidity):
            self.ids.humidity.text = humidity+"%"

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
            str(start["hour"]) + ":" + str(start["minute"])
        self.ids.day_end.text = "DAY FINISHES AT " + \
            str(end["hour"]) + ":" + str(end["minute"])

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
