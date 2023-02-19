import RPi.GPIO as GPIO


class LedLamp:
    def __init__(self):
        self.LED_PIN = 17
        self.status = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        GPIO.output(self.LED_PIN, GPIO.LOW)

    def on(self):
        GPIO.output(self.LED_PIN, GPIO.HIGH)
        self.set_status(1)

    def off(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
        self.set_status(0)

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status
