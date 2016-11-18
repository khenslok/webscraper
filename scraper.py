import os
from lxml import html
import requests
import re
from country import Country

class Scraper:
    URL = 'https://www.federalreserve.gov/releases/h10/hist/'
    TABLE_ROW = '//table[@class="statistics"]/tr'
    COUNTRY_NAME = '*/a[@href]/text()'
    UNIT_NAME = 'td/text()'
    LINK = '*/a/@href'
    DATE = '*[@id="r1"]/text()'
    VALUE = 'td[@headers="a2 a1 r1"]/text()'

    def __init__(self, output):
        self.output = output


    def scrape(self):
        page = requests.get(Scraper.URL)
        tree = html.fromstring(page.content)
        for elem in tree.xpath(Scraper.TABLE_ROW):
            c = Country(elem.xpath(Scraper.COUNTRY_NAME)[0], elem.xpath(Scraper.UNIT_NAME)[0], elem.xpath(Scraper.LINK)[0])
            self.populateRatingsForCountry(c)
            self.writeToFile(c)


    def populateRatingsForCountry(self, c):
        print "Populating %s" % c.name
        page = requests.get(Scraper.URL + c.link)
        tree = html.fromstring(page.content)
        for elem in tree.xpath(Scraper.TABLE_ROW):
            d = re.search("(\d+-[a-zA-Z]{3}-\d\d)", elem.xpath(Scraper.DATE)[0]).group()
            v = re.search("\d+\.\d+|[a-zA-Z]+", elem.xpath(Scraper.VALUE)[0]).group()
            c.addRate(d, v)


    def writeToFile(self, c):
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        filename = self.output + c.name + ".json"
        f = open(filename, 'w')
        print >> f, c.toJsonObject()
        f.close()

if __name__ == "__main__":
    scraper = Scraper("output/")
    scraper.scrape()