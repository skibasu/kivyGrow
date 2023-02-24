import board
import adafruit_dht
from Humidifier.Humidifier import Humidifier
import asyncio

humidifier = Humidifier()


class Weather:

    def __init__(self, app_config):
        self.app_config = app_config
        self.dht_device = adafruit_dht.DHT22(board.D27)
        self.temperature = 0
        self.humidity = 0

        self.check_temp_and_humidity()

    def check_temp_and_humidity(self):
        try:
            temp = self.dht_device.temperature
            hum = self.dht_device.humidity

            period = self.app_config["get_period"]()
            ranges = self.app_config["get_ranges_of_humidity"]()

            f_min_humidity = float(ranges["flowering"]["humidity_min"])
            f_max_humidity = float(ranges["flowering"]["humidity_max"])
            v_min_humidity = float(ranges["vegetative"]["humidity_min"])
            v_max_humidity = float(ranges["vegetative"]["humidity_max"])

            self.temperature = temp
            self.humidity = hum

            if (period == 12):

                if ((type(hum) == int or type(hum) == float) and hum < f_min_humidity):
                    humidifier.on()
                elif ((type(hum) == int or type(hum) == float) and hum > f_max_humidity):
                    humidifier.off()

            if (period == 18):

                if ((type(hum) == int or type(hum) == float) and hum < v_min_humidity):
                    humidifier.on()
                elif ((type(hum) == int or type(hum) == float) and hum > v_max_humidity):
                    humidifier.off()

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            pass

        except Exception as error:
            raise error

    def get_temp_hum(self):
        return [self.temperature, self.humidity]

    def destroy(self):
        self.dht_device.exit()
