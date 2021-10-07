import requests

def exchange_rates(val):
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    response = response.json()
    return response.get('Valute')[val].get('Value')

if __name__ == '__main__':
    USD = exchange_rates('USD')
    KZT = exchange_rates('KZT')

    print(USD, KZT)