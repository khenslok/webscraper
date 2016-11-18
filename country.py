class Country:
    'Common base class for country'

    def __init__(self, name, unit, link):
        self.name = name
        self.unit = unit
        self.link = link

    def setRates(self, rates):
        self.rates = rates

    def displayCountry(self):
        print "Name ", self.name, " unit: ", self.unit, " link: ", self.link, " rates: "
        for r in self.rates:
            r.displayRate()

