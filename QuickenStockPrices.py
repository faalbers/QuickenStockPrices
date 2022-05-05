import pandas as pd
import yfinance as yf

importFile = open('Z:\\Quicken\\QuickenExport.QIF')

isSecurity = False
isQuote = False
quotes = set()
for line in importFile.readlines():
    if isQuote:
        quotes.add(line.strip()[1:])
        isSecurity = False
        isQuote = False
    elif isSecurity:
        isQuote = True
    elif line.startswith('!Type:Security'):
        isSecurity = True
importFile.close()

qPrices = {}
for quote in quotes:
    if quote == 'Cash':
        continue
    data = yf.download(quote, period='5d')
    if data['Close'].size > 0:
        qPrices[quote] = data['Close'][data['Close'].size-1]

exportFile = open('Z:\\Quicken\\QuickenImport.csv', 'w')
for qPrice in qPrices:
    exportFile.write('%s, %.3f\n' % (qPrice, qPrices[qPrice]))
    #print('%s, %.3f' % (qPrice, qPrices[qPrice]))
exportFile.close()
