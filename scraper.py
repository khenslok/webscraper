import os

from lxml import html
import requests
import country
import rate
import re
import json

url = 'https://www.federalreserve.gov/releases/h10/hist/'
countries = []


page = requests.get(url)
tree = html.fromstring(page.content)

for elem in tree.xpath('//table[@class="statistics"]/tr'):
    countries.append(country.Country(elem.xpath('th/a[@href]/text()')[0], elem.xpath('td/text()')[0], elem.xpath('th/a/@href')[0]))

for c in countries:
    page = requests.get(url + c.link)
    tree = html.fromstring(page.content)
    rates = []
    for elem in tree.xpath('//table[@class="statistics"]/tr'):
        d = re.findall("(\d+-[a-zA-Z]{3}-\d\d)", elem.xpath('th[@id="r1"]/text()')[0])[0]
        v = re.findall("\d+\.\d+|[a-zA-Z]+", elem.xpath('td[@headers="a2 a1 r1"]/text()')[0])[0]
        rates.append(rate.Rate(d, v))
    c.setRates(rates)

def encode_rate(obj):
    if isinstance(obj, rate.Rate):
        return obj.__dict__
    return obj

if not os.path.exists("output"):
    os.makedirs("output")

for c in countries:
    s = json.dumps(c.__dict__, default=encode_rate)
    filename = "output/" +c.name + ".json"
    f = open(filename, 'w')
    print >> f, s
    f.close()