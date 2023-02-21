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
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "600")

app_config = ConfigApp()
led_lamp = LedLamp()
time_of_the_day = TimeOfTheDay()
weather = Weather()
clock = ClockApp({"get_range": app_config.get_range}, {
    "led_lamp": led_lamp, "time_of_the_day": time_of_the_day})


class MainScreen(Screen):
    app_is_runnig = app_config.get_is_running()
    period = app_config.get_period()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def on_parent(self, widget, parent):
        self.init_ui()
        self.update_clock()
        self.update_weather()
        BackgroundClock.schedule_interval(self.update_clock, 1)
        BackgroundClock.schedule_interval(self.update_weather, 3)

    def init_ui(self, args=None):
        self.add_start_button_styles()
        self.set_time()
        self.set_calendar()
        self.initialize_day_time()

    def init_after_app_start(self):
        self.initialize_start_end()

    def set_time(self, args=None):
        self.ids.clock.text = clock.get_time()

    def update_clock(self, args=None):
        clock.set_time()
        self.set_time()

        if (app_config.get_is_running()):
            print('updating clock')
            clock.check_range()
            self.update_day_icon()

    def update_weather(self, args=None):
        temperature = weather.get_temp_hum()[0]
        temperature_str = str(temperature)
        humidity = weather.get_temp_hum()[1]
        humidity_str = str(humidity)
        weather.check_temp_and_humidity()

        if ((type(temperature) == int or type(temperature) == float) and self.ids.temperature.text != temperature_str):
            self.ids.temperature.text = temperature_str+"\N{DEGREE SIGN}C"
            self.ids.temperature.progress = -140 + \
                temperature * 5.6
            self.set_temp_colors(temperature)

        if ((type(humidity) == int or type(humidity) == float) and self.ids.humidity.text != humidity_str):
            self.ids.humidity.text = humidity_str+"%"
            self.ids.humidity.progress = -140 + humidity * 2.8
            self.set_hum_colors(humidity)

    def set_temp_colors(self, temp):
        is_lamp_on = led_lamp.get_status()
        self.period = app_config.get_period()

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

        elif not is_lamp_on and self.period != None:
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
        else:
            self.ids.temperature.progress_color = (
                229 / 253, 146 / 253, 12 / 253, 1)

    def set_hum_colors(self, hum):
        self.period = app_config.get_period()

        if self.period == 18:
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

        elif self.period == 12:
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
        else:
            self.ids.humidity.progress_color = (
                32 / 253, 87 / 253, 211 / 253, 1)

    def set_calendar(self):

        self.ids.calendar.text = clock.get_calendar()

    def toggle_day_icon(self):
        self.time_of_the_day_source = time_of_the_day.get_icon()

    def update_day_icon(self):
        if (time_of_the_day.get_icon() != self.time_of_the_day_source):
            self.toggle_day_icon()

    def initialize_day_time(self):
        if app_config.get_is_running():
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

    def add_start_button_styles(self):
        if (self.app_is_runnig):
            self.ids.start_btn.text = "END GROW"
            self.ids.start_btn.background_color = [
                199 / 253, 68 / 253, 73 / 253, 1]

        else:
            self.ids.start_btn.text = "START GROW"
            self.ids.start_btn.background_color = [
                73 / 253, 106 / 253, 72 / 253, 1]

    def toggle_start(self):
        self.add_start_button_styles()


class SettingsScreen(Screen):

    app_is_runnig = app_config.get_is_running()
    period = app_config.get_period()

    def __init__(self, **kwargs):

        super(SettingsScreen, self).__init__(**kwargs)

    def on_parent(self, widget, parent):
        self.initialize_start_time()

    def start_vegetative(self):
        start_time = {"hour": int(self.ids.config_start_hour.text), "minute": int(
            self.ids.config_start_minute.text)}
        print(start_time)
        app_config.set_period("vegetative")
        app_config.set_start_time(start_time)
        app_config.set_end_time()
        app_config.start_is_running()

        self.initialize_start_time()

        self.app_is_runnig = app_config.get_is_running()
        self.period = app_config.get_period()

        print("START", self.app_is_runnig)

    def start_flowering(self):
        pass

    def initialize_start_time(self):
        range = app_config.get_range()
        start = range[0]

        if (start != ""):
            self.ids.config_start_hour.text = time(
                start["hour"]).strftime("%H")
            self.ids.config_start_minute.text = time(
                start["minute"]).strftime("%M")
        else:
            self.ids.config_start_hour.text = "00"
            self.ids.config_start_minute.text = "00"

    def add_hour(self):
        h = int(self.ids.config_start_hour.text)

        if (h == 23):
            h = 0
        else:
            h = h + 1

        self.ids.config_start_hour.text = time(h).strftime("%H")

    def minus_hour(self):
        h = int(self.ids.config_start_hour.text)

        if (h == 0):
            h = 23
        else:
            h = h - 1

        self.ids.config_start_hour.text = time(h).strftime("%H")

    def add_minute(self):
        m = int(self.ids.config_start_minute.text)

        if (m == 59):
            m = 0
        else:
            m = m + 1

        self.ids.config_start_minute.text = time(0, m).strftime("%M")

    def minus_minute(self):
        m = int(self.ids.config_start_minute.text)

        if (m == 0):
            m = 59
        else:
            m = m - 1

        self.ids.config_start_minute.text = time(0, m).strftime("%M")

    def add_humidity(self, element, period):
        h = int(element.text)

        if h == 99:
            h = 99

        else:
            h = h + 1

        element.text = str(h)
        self.humidity_validation(period)

    def minus_humidity(self, element, period):

        h = int(element.text)

        if h == 0:
            h = 0

        else:
            h = h - 1
        element.text = str(h)
        self.humidity_validation(period)

    def humidity_validation(self, period):
        if (period == "VEGETATION"):
            h_min_v = int(self.ids.v_min_humidity.text)
            h_max_v = int(self.ids.v_max_humidity.text)

            if (h_min_v == h_max_v - 1):
                self.ids.b_v_min_plus.disabled = True
                self.ids.b_v_max_minus.disabled = True

            else:
                self.ids.b_v_min_plus.disabled = False
                self.ids.b_v_max_minus.disabled = False

        if (period == "FLOWERING"):
            h_min_f = int(self.ids.f_min_humidity.text)
            h_max_f = int(self.ids.f_max_humidity.text)

            if (h_min_f == h_max_f - 1):
                self.ids.b_f_min_plus.disabled = True
                self.ids.b_f_max_minus.disabled = True

            else:
                self.ids.b_f_min_plus.disabled = False
                self.ids.b_f_max_minus.disabled = False


class StatisticsWidget(Screen):
    def __init__(self, **kwargs):
        super(StatisticsWidget, self).__init__(**kwargs)


class GrowboxApp(App):

    def build(self):

        sm = ScreenManager(transition=NoTransition())

        sm.add_widget(MainScreen(name="MainScreen"))
        sm.add_widget(SettingsScreen(name="SettingsScreen"))
        sm.add_widget(StatisticsWidget(name="StatisticsWidget"))

        return sm


if __name__ == '__main__':
    GrowboxApp().run()
