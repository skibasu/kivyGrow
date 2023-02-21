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
