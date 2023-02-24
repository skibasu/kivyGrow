import httpx
import asyncio
from FanIn.FanIn import FanIn


class Humidifier():
    def __init__(self):
        self.is_on = False
        self.fan = FanIn()

    def on(self):
        if self.is_on == False:
            asyncio.run(self.request_on())
            self.fan.on()

    def off(self):
        if self.is_on == True:
            asyncio.run(self.request_off())
            self.fan.off()

    def get_status(self):
        return self.is_on

    def set_status(self, status):
        self.is_on = status

    async def request_on(self):
        async with httpx.AsyncClient() as client:
            await client.get("https://maker.ifttt.com/trigger/turn_on_1/json/with/key/cOsvpHzPfWSa2EnmRjbXdO")
            self.set_status(True)

    async def request_off(self):
        async with httpx.AsyncClient() as client:
            await client.get("https://maker.ifttt.com/trigger/turn_off_1/json/with/key/cOsvpHzPfWSa2EnmRjbXdO")
            self.set_status(False)
