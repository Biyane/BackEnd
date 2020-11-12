from random import *
from django.http import HttpResponse
import requests
import json
from datetime import datetime as dt
import datetime
import time
import urllib.parse as urlparse
from urllib.parse import parse_qs


flyDir = [
    ['ALA', 'TSE'],
    ['TSE', 'ALA'],
    ['ALA', 'MOW'],
    ['MOW', 'ALA'],
    ['ALA', 'CIT'],
    ['CIT', 'ALA'],
    ['TSE', 'MOW'],
    ['MOW', 'TSE'],
    ['TSE', 'LED'],
    ['LED', 'TSE'],
]
booking_url = 'https://api.skypicker.com/flights'
my_arr = []
my_stack = []

# Журнал самых дешевых билетов на выбранный день на все пути
def aviata_booking_test(request):
    for fly in flyDir:
        min_price = 99999
        booking_token = ""
        params = {'fly_from': 'JFK', 'fly_to': 'MCO', 'partner': 'picky', 'date_from': '13/12/2020',
                  'date_to': '24/12/2020', 'adults': 1, 'infants': 1}
        start_time = time.time()
        print(start_time)
        response = requests.get(url=booking_url, params=params)
        print(time.time() - start_time)
        parsed = urlparse.urlparse(response.url)
        print(type(parse_qs(parsed.query)['infants'][0]))
        print(parse_qs(parsed.query)['infants'][0])
        if response.status_code == 200:
            data = json.loads(response.text)
            for dic in data['data']:
                return HttpResponse(json.dumps(dic))
                temp_price = dic['price']
                if temp_price < min_price:
                    min_price = temp_price
                    booking_token = dic['booking_token']
            temp_dic = {'fly_from': 'ALA', 'fly_to': 'TSE', 'price': min_price,
                        'booking_token': booking_token}
            #вызвать price_confirmation
            my_arr.append(temp_dic)
        else:
            return HttpResponse("ups, wrong request oh something happened that is not good for you)")
    return HttpResponse(json.dumps(my_arr, indent=4))


# date_now = dt.now()
# date_on = date_now + datetime.timedelta(days=randrange(5, 30))
# date_to = date_on.strftime('%d/%m/%Y')
# print(date_on.strftime('%d/%m/%Y'))
# a = str(date_on).split(" ")[0].split('-')
# print('/'.join(a))
# print(date_to)


def aviata_booking_for_month(request):
    date_now = dt.now() + datetime.timedelta(days=0)
    for i in range(31):
        date_on = date_now + datetime.timedelta(days=randrange(5, 30))
        date_to = '/'.join(str(date_on).split(" ")[0].split('-')[::-1])
        date_from = '/'.join(str(date_now).split(" ")[0].split('-')[::-1])
        min_price = 9999
        params = {'fly_from': flyDir[0][0], 'fly_to': flyDir[0][1], 'partner': 'picky', 'date_from': date_from,
                  'date_to': date_to, 'adults': 1, 'infants': 1}
        try:
            start_time_response = time.time()
            response = requests.get(url=booking_url, params=params)
            parsed = urlparse.urlparse(response.url)
            print(time.time() - start_time_response, '<--------------------')
            if response.status_code == 200:
                data = json.loads(response.text)
                for dic in data['data']:
                    temp_price = dic['price']
                    if temp_price < min_price:
                        min_price = temp_price
                        booking_token = dic['booking_token']
                        adults = parse_qs(parsed.query)['adults'][0]
                        infants = parse_qs(parsed.query)['infants'][0]
                        conversion = dic['conversion'].keys()
                        my_stack.append({'fly_from': flyDir[0][0],
                                         'fly_to': flyDir[0][1],
                                         'price': min_price,
                                         'booking_token': booking_token,
                                         'adults': adults,
                                         'infants': infants,
                                         'bnum': len(dic['bags_price']),
                                         'currency': list(conversion)[0]})
                flights_checked(request)
                validated = False
                while my_stack:
                    i = 0
                    while i < 5:
                        validated = flights_checked(request)
                        if validated:
                            break
                        i += 1
                    if validated:
                        break
                    my_stack.pop()
                if my_stack:
                    length = len(my_stack) - 1
                    print({'price': my_stack[length]['price'],
                           'booking_token': my_stack[length]['booking_token']})
                    my_arr.append(my_stack[len(my_stack)])
            else:
                return HttpResponse("oops something wrong happened")
            date_now += datetime.timedelta(days=1)
        except requests.exceptions.ConnectionError:
            raise ConnectionError("yeah...")
    return HttpResponse(json.dumps(my_arr, indent=4))


def flights_checked(request):
    print('hello from flights_checked')
    start_time_response = time.time()
    check_price_url = 'https://booking-api.skypicker.com/api/v0.1/check_flights'
    length = len(my_stack) - 1
    params = {'v': 2,
              'booking_token': my_stack[length]['booking_token'],
              'bnum': my_stack[length]['bnum'],
              'pnum': 2,
              'currency': my_stack[length]['currency'],
              'adults': my_stack[length]['bnum'],
              'children': 1,
              'infants': my_stack[length]['infants']}
    print(params)
    try:
        r = requests.get(url=check_price_url, params=params)
        print(time.time() - start_time_response)
        print(r.text)
        my_json = json.loads(r.text)
        if my_json['price_change'] == 'true':
            my_stack[length]['price'] = my_json['flights_price']
        return my_json['flights_checked'] == 'true' and my_json['flights_invalid'] == 'true'
    finally:
        raise ConnectionError("uuuppsssss")


def test(request):
    params = {'fly_from': flyDir[0][0], 'fly_to': flyDir[0][1], 'partner': 'picky', 'date_from': '13/12/2020',
              'date_to': '24/12/2020', 'adults': 1, 'infants': 1}
    response = requests.get(url=booking_url, params=params)
    return HttpResponse(response.text)


# date_now = dt.now() + datetime.timedelta(days=0)
# for i in range(31):
#     # date_on = date_now + datetime.timedelta(days=randrange(5, 30))
#     # a = str(date_on).split(" ")[0].split('-')[::-1]
#     # date_to = '/'.join(a)
#     date_from = '/'.join(str(date_now).split(" ")[0].split('-')[::-1])
#     print(date_from)
#     date_now += datetime.timedelta(days=1)






# time = localtime(now())
# date = dt.now()
# date2 = time - datetime.timedelta(days=30)
# date3 = datetime.datetime(2020, 12, 12, 00, 00, 00)
# print(date3)
# print(date2)
# print(time)
# print(date)
# print(date.strftime('%d/%m/%Y'))

