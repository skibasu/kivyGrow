

class TimeOfTheDay:
    def __init__(self):
        self.status = "night"
        self.night_image = "assets/m.png"
        self.day_image = "assets/s.png"

    def get_icon(self):
        if self.status == 'day':
            return self.day_image

        elif self.status == 'night':
            return self.night_image

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status
