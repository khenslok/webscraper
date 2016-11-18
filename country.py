from rate import Rate
import json


class Country:
    'Common base class for all countries'

    def __init__(self, name, unit, link):
        self.name = name
        self.unit = unit
        self.link = link
        self.rates = []

    def addRate(self, date, value):
        self.rates.append(Rate(date, value))

    def displayCountry(self):
        print "Name ", self.name, " unit: ", self.unit, " link: ", self.link, " rates: "
        for r in self.rates:
            r.displayRate()

    def toJsonObject(self):
        return json.dumps(self.__dict__, default=Rate.encode_rate, indent=4, sort_keys=True)
