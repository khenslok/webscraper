class Rate:
    'Common base class for historic rates'
    def __init__(self, date, value):
        self.date = date
        self.value = value

    def displayRate(self):
        print self.date, " ", self.value