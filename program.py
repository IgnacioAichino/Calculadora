from tokenize import Double
import requests
from datetime import date
from datetime import timedelta
import json
import sys
from ctypes import *

def getCryptoFromUser():
    print('Elija la criptomoneda de la cual desea conocer el valor')
    print('BTC: Bitcoin')
    print('ETH: Ethereum')
    print('ADA: Cardano')
    crypto = input()
    while crypto not in ['BTC', 'ETH', 'ADA']:
        print('Criptomoneda ingresada no valida\n')
        crypto = input()
    return crypto

def getCurrencyFromUser():
    print('\nLa moneda en la que desea el resultado')
    print('USD: Dolar')
    print('EUR: Euro')
    print('ARS: Pesos Argentinos')
    currency = input()
    while currency not in ['USD', 'EUR', 'ARS']:
        print('Moneda ingresada no valida\n')
        currency = input()
    return currency

def getPriceFromUrl(url):
    return json.loads(requests.get(url).text)["results"][0]["c"]

def existsDataForToday(today_url):
    return "results" in json.loads(requests.get(today_url).text)

if len(sys.argv) == 1:
 
    today = date.today().strftime('%Y-%m-%d')
    yesterday = (date.today() - timedelta(days = 1)).strftime('%Y-%m-%d')
    apiKey = 'yL5W34yMGGETZMTXS3toirNXLx5SIpL6'

    crypto = getCryptoFromUser()
    crypto_url = 'https://api.polygon.io/v2/aggs/ticker/X:' + crypto + 'USD/range/1/minute/' + today + '/' + today + '?sort=desc&limit=1&apiKey=' + apiKey
    crypto_url_yestarday = 'https://api.polygon.io/v2/aggs/ticker/X:' + crypto + 'USD/range/1/minute/' + yesterday + '/' + yesterday + '?sort=desc&limit=1&apiKey=' + apiKey
    crypto_price = getPriceFromUrl(crypto_url) if existsDataForToday(crypto_url) else getPriceFromUrl(crypto_url_yestarday)

    currency = getCurrencyFromUser()
    currency_url = 'https://api.polygon.io/v2/aggs/ticker/C:USD' + currency + '/range/1/minute/' + today + '/' + today + '?adjusted=true&sort=desc&limit=1&apiKey=' + apiKey
    currency_url_yestarday = 'https://api.polygon.io/v2/aggs/ticker/C:USD' + currency + '/range/1/minute/' + yesterday + '/' + yesterday + '?adjusted=true&sort=desc&limit=1&apiKey=' + apiKey
    currency_price = 1.0 if currency == 'USD' else (getPriceFromUrl(currency_url) if existsDataForToday(currency_url) else getPriceFromUrl(currency_url_yestarday))
elif len(sys.argv) == 3: # this if is only for testing

    today = '2022-04-05'
    crypto = 'BTC'
    currency = 'EUR'
    crypto_price = float(sys.argv[1])
    currency_price = float(sys.argv[2])

converter = CDLL("./converter.so")
converter.convert.argtypes = [c_float, c_float]
converter.convert.restype = c_double

result = converter.convert(crypto_price, currency_price)

print('Fecha de la consulta: ' + today)
print('Precio de la cryptomoneda ' + crypto + ': ' + str(crypto_price) + 'USD')
print('Precio de la moneda: ' + str(currency_price) + currency + ' --> 1USD')
print('Precio de la cryptomoneda en ' + currency + ': ' + str(round(result, 4)))
