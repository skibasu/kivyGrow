import board
import adafruit_dht


class Weather:

    def __init__(self):

        self.dht_device = adafruit_dht.DHT22(board.D27)
        self.temperature = 0
        self.humidity = 0

        self.check_temp_and_humidity()

    def check_temp_and_humidity(self):
        try:
            temp = self.dht_device.temperature
            hum = self.dht_device.humidity

            self.temperature = temp
            # self.set_temp_colors(temp)
            # self.set_hum_colors(hum)
            self.humidity = hum

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            pass

        except Exception as error:
            raise error

    def get_temp_hum(self):
        return [self.temperature, self.humidity]

    def destroy(self):
        self.dht_device.exit()

    def set_temp_colors(self, temp):
        is_lamp_on = self.config["is_lamp_on"]()

        if is_lamp_on:
            if temp > 0 and temp < 18:
                self.temperature_meter.set_style('info')
            elif temp >= 18 and temp <= 28:
                self.temperature_meter.set_style('warning')
            elif temp > 28:
                self.temperature_meter.set_style('danger')
        else:
            if temp < 16:
                self.temperature_meter.set_style('info')
            if temp >= 16 and temp < 22:
                self.temperature_meter.set_style('warning')
            elif temp >= 22:
                self.temperature_meter.set_style('danger')

    def set_hum_colors(self, hum):
        period = self.config["get_period"]()

        if period == 18:
            if hum > 0 and hum < 50:
                self.humidity_meter.set_style('info')
            elif hum >= 50 and hum <= 75:
                self.humidity_meter.set_style('primary')
            elif hum > 28:
                self.humidity_meter.set_style('danger')

        else:
            if hum > 0 and hum < 40:
                self.humidity_meter.set_style('info')
            elif hum >= 40 and hum <= 50:
                self.humidity_meter.set_style('primary')
            elif hum > 50:
                self.humidity_meter.set_style('danger')
