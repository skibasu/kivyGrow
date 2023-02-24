from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from ConfigApp.ConfigApp import ConfigApp
from ClockApp.ClockApp import Clock as ClockApp
from LedLamp.LedLamp import LedLamp
from kivy.clock import Clock as BackgroundClock
from TimeOfTheDay.TimeOfTheDay import TimeOfTheDay
from Weather.Weather import Weather
from datetime import time
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.popup import Popup
from kivy.factory import Factory
from api.api import Api
from datetime import datetime

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "600")

api = Api()
app_config = ConfigApp()
led_lamp = LedLamp()
time_of_the_day = TimeOfTheDay()
weather = Weather()
clock = ClockApp({"get_range": app_config.get_range, "set_current_day": app_config.set_current_day}, {
    "led_lamp": led_lamp, "time_of_the_day": time_of_the_day})


class ConfirmationPopup(Popup):

    def confirm(self, action):
        self.action()

    def set_action(self, action):
        self.action = action


class SavedPopup(Popup):
    def confirm(self, action):
        self.action()

    def set_action(self, action):
        self.action = action


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

    def on_pre_enter(self):
        self.initialize_start_end()

        if (app_config.get_period()):
            self.add_start_button_styles()

    def close_app(self):
        App.get_running_app().stop()
        Window.close()

    def open_popup(self):
        popup = Factory.ConfirmationPopup()
        popup.set_action(self.close_app)
        popup.open()

    def start_to_grow(self):
        if not app_config.get_is_running():
            self.manager.current = "SettingsScreen"
        else:
            self.open_popup()

    def init_ui(self, args=None):
        self.set_time()
        self.set_calendar()
        self.initialize_day_time()

    def set_time(self, args=None):
        self.ids.clock.text = clock.get_time()

    def update_clock(self, args=None):
        clock.set_time()
        self.set_time()

        if (app_config.get_is_running()):
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
        self.count_days()

    def count_days(self):
        if (time_of_the_day.get_icon() == "assets/s.png"):
            current_time = datetime.now()
            started_at = app_config.get_started_at()
            current_day = app_config.get_current_day()
            period = app_config.get_period()

            delta = current_time - started_at
            print("DELTA", delta)

            if ((delta.days + 1) > current_day):
                app_config.set_current_day(current_day+1)
                self.ids.all_days_counter.text = str(
                    app_config.get_current_day()) + "th day of grow"

                if (period == 12):
                    api.increment_day('current_f_day')
                    app_config.set_current_v_day(
                        app_config.get_current_f_day() + 1)
                    self.ids.f_days.text = "FLOWERING:" + \
                        str(app_config.get_current_f_day()) + "th DAY"

                elif (period == 18):
                    api.increment_day('current_v_day')
                    app_config.set_current_v_day(
                        app_config.get_current_v_day() + 1)
                    self.ids.v_days.text = "VEGETATION:" + \
                        str(app_config.get_current_v_day()) + "th DAY"

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
        if app_config.get_is_running():
            range = app_config.get_range()
            start = range[0]
            end = range[1]

            self.ids.all_days_counter.text = str(
                app_config.get_current_day()) + "th day of grow"

            self.ids.v_days.text = "VEGETATION: " + \
                str(app_config.get_current_v_day()) + "th DAY"

            self.ids.f_days.text = "FLOWERING: " + \
                str(app_config.get_current_f_day()) + "th DAY"

            self.ids.day_start.text = "DAY STARTS AT " + \
                time(start["hour"], start["minute"]).strftime("%H:%M")
            self.ids.day_end.text = "DAY FINISHES AT " + \
                time(end["hour"], end["minute"]).strftime("%H:%M")

    def add_start_button_styles(self):
        self.ids.start_btn.text = "END GROW"
        self.ids.start_btn.background_color = [
            199 / 253, 68 / 253, 73 / 253, 1]


class SettingsScreen(Screen):

    def __init__(self, **kwargs):

        super(SettingsScreen, self).__init__(**kwargs)

    def on_parent(self, widget, parent):
        self.initialize_start_time()

    def on_pre_enter(self):
        self.update_humidity_ranges()
        self.update_btns_disabled()

    def update_humidity_ranges(self):
        ranges = app_config.get_ranges_of_humidity()
        f_min_humidity = ranges["flowering"]["humidity_min"]
        f_max_humidity = ranges["flowering"]["humidity_max"]
        v_min_humidity = ranges["vegetative"]["humidity_min"]
        v_max_humidity = ranges["vegetative"]["humidity_max"]

        self.ids.f_min_humidity.text = f_min_humidity
        self.ids.f_max_humidity.text = f_max_humidity
        self.ids.v_min_humidity.text = v_min_humidity
        self.ids.v_max_humidity.text = v_max_humidity

    def update_btns_disabled(self):
        if (app_config.get_period() == 18):
            self.ids.b_start_vegetative.disabled = True
            self.ids.b_start_flowering.disabled = False
        elif (app_config.get_period() == 12):
            self.ids.b_start_flowering.disabled = True
            self.ids.b_start_vegetative.disabled = True

        if (app_config.get_is_running()):

            self.lock_time_picker()

    def save_humidity_ranges(self):
        ranges = {"vegetative": {"humidity_min": self.ids.v_min_humidity.text, "humidity_max": self.ids.v_max_humidity.text},
                  "flowering": {"humidity_min": self.ids.f_min_humidity.text, "humidity_max": self.ids.f_max_humidity.text}}
        app_config.set_ranges_of_humidity(ranges)

        self.update_humidity_ranges()
        api.update_config(ranges)
        self.open_popup_saved()

    def start_vegetative(self, popup):

        start_time = {"hour": int(self.ids.config_start_hour.text), "minute": int(
            self.ids.config_start_minute.text)}
        app_config.set_period("vegetative")
        app_config.set_start_time(start_time)
        app_config.set_end_time()
        app_config.start_is_running()
        app_config.set_started_at()

        self.initialize_start_time()
        self.lock_time_picker()
        self.ids.b_start_vegetative.disabled = True
        self.ids.b_start_flowering.disabled = False
        api.update_config({"start": start_time, "period": 18,
                          "end": app_config.get_range()[1], "is_running": True,  "started_at": datetime.now()})
        popup.dismiss()

    def open_popup_saved(self):
        popup = Factory.SavedPopup()
        popup.set_action(lambda popup=popup: self.go_to_main_screen(popup))
        popup.open()

    def go_to_main_screen(self, popup):
        popup.dismiss()
        self.manager.current = "MainScreen"

    def open_popup_vegetative(self):
        popup = Factory.ConfirmationPopup()
        popup.set_action(lambda popup=popup: self.start_vegetative(popup))
        popup.open()

    def open_popup_flowering(self):
        popup = Factory.ConfirmationPopup()
        popup.set_action(lambda popup=popup: self.start_flowering(popup))
        popup.open()

    def start_flowering(self, popup):
        app_config.set_period("flowering")
        app_config.set_end_time()

        self.ids.b_start_flowering.disabled = True
        api.update_config({"period": 12, "end": app_config.get_range()[1]})
        popup.dismiss()

    def lock_time_picker(self):
        self.ids.b_add_hour.disabled = True
        self.ids.b_minus_hour.disabled = True
        self.ids.b_add_minute.disabled = True
        self.ids.b_minus_minute.disabled = True

    def initialize_start_time(self):
        range = app_config.get_range()
        start = range[0]

        if (start != ""):
            self.ids.config_start_hour.text = time(
                start["hour"]).strftime("%H")
            self.ids.config_start_minute.text = time(
                start["hour"], start["minute"]).strftime("%M")
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
    icon = "icon.png"

    def build(self):

        self.sm = ScreenManager(transition=NoTransition())
        self.main_screen = MainScreen(name="MainScreen")
        self.settings_screen = SettingsScreen(name="SettingsScreen")

        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.settings_screen)
        self.sm.add_widget(StatisticsWidget(name="StatisticsWidget"))

        return self.sm


if __name__ == '__main__':
    GrowboxApp().run()
