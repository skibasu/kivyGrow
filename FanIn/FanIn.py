import httpx
import asyncio


class FanIn():
    def __init__(self):
        self.is_on = False

    def on(self):
        if self.is_on == False:
            asyncio.run(self.request_on())

    def off(self):
        if self.is_on == True:
            asyncio.run(self.request_off())

    def get_status(self):
        return self.is_on

    def set_status(self, status):
        self.is_on = status

    async def request_on(self):
        async with httpx.AsyncClient() as client:
            await client.get("https://maker.ifttt.com/trigger/turn_on_3/json/with/key/cOsvpHzPfWSa2EnmRjbXdO")
            self.set_status(True)

    async def request_off(self):
        async with httpx.AsyncClient() as client:
            await client.get("https://maker.ifttt.com/trigger/turn_off_3/json/with/key/cOsvpHzPfWSa2EnmRjbXdO")
            self.set_status(False)
