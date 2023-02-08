import requests
import time

'''Функция конвертирующая валюту'''
'''api_access_token - api qiwi токен, sum_exchange - сумма конвертации(тоесть если вам нужно получить 100 тенге из имеющихся у вас рублей -  пишите 100
 currency - код валюты в которую конвертируете,  to_qw номер телефона вашего счета'''
def exchange(api_access_token, sum_exchange, currency, to_qw):
    s = requests.Session()
    currencies = ['398', '840', '978']
    if currency not in currencies:
      print('This currency not available')
      return
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + api_access_token
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept'] = 'application/json'
    postjson = {"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"}, "comment":"'+comment+'","fields":{"account":""}}
    postjson['id'] = str(int(time.time() * 1000))
    postjson['sum']['amount'] = sum_exchange
    postjson['sum']['currency'] = currency
    postjson['fields']['account'] = to_qw
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/1099/payments', json = postjson)
    print(f'Осущетсвлен перевод валют.Переведено {rate_of_exchange(api_access_token,"398","643")*sum_exchange} рублей в {sum_exchange} тенге')
    return res.json()


'''Функция курса валют'''
def rate_of_exchange(api_access_token, currency_to, currency_from):
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + api_access_token
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept'] = 'application/json'
    res = s.get('https://edge.qiwi.com/sinap/crossRates')

    # все курсы
    rates = res.json()['result']

    # запрошенный курс
    rate = [x for x in rates if x['from'] == currency_from and x['to'] == currency_to]
    if (len(rate) == 0):
        print('No rate for this currencies!')
        return
    else:
        print(f'Курс валют 1 Р к {rate[0]["rate"]} тенге')
        return rate[0]['rate']


'''Реализация пополнения стим аккаунта'''
def send_steam(login: str, API_TOKEN,PAYMENT) -> dict:
    s = requests.Session()
    s.headers['Accept'] = 'application/json'
    s.headers['Content-Type'] = 'application/json'
    s.headers['authorization'] = 'Bearer ' + API_TOKEN

    postjson = {"id":"","sum": {"amount":"","currency":"398"},"paymentMethod": {"type":"Account","accountId":"398"},"fields": {"account":""}}
    postjson['id'] = str(int(time.time() * 1000))
    postjson['sum']['amount'] = str(PAYMENT)
    postjson['fields']['account'] = login

    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/31212/payments', json = postjson)
    # If exception simplejson.errors.JSONDecodeError recheck qiwi api token
    return res.json()


'''Пополнение стим и информация о нем, для пополнения вызывайте эту функцию'''
def pay_to_steam(account, payment, api_token):
    print(f'Аккаунт:{account}')
    print("(Данные о пополнении)response:", send_steam(account, api_token, payment))
    print("Well done!")


