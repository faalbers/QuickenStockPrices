import sys
from os.path import dirname
sys.path.append(dirname(__file__))

from qifparse.parser import QifParser
from alpha_vantage.timeseries import TimeSeries
import time

ts = TimeSeries(key='5I186NCN3TF27H5P', output_format='csv')
file = open('QuickenExport.QIF')
qif = QifParser.parse(file)

print("Parsed it ...")

quotes = set()
for price in qif.get_prices():
    quotes.add(price.name)

print(quotes)

newquotes = {}
outstring = ""
for quote in quotes:
    data, meta_data = ts.get_quote_endpoint(quote)
    data = list(data)
    if len(data) == 2:
        price = float(list(data)[1][4])
        #print(quote)
        outstring += "%s, %.3f\n" % (quote, price)
    # unpayed acces to apha vantage needs 12 seconds between every parse
    time.sleep(12)
outfile = open('LatestStockPrices.csv', 'w')
outfile.write(outstring)
file.close()
