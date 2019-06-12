# -*- coding: utf-8 -*-
import requests

def geocode(address, key):
    '''
    https://developers.google.com/maps/documentation/geocoding/start
    '''
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': address, 'key':key}
    r = requests.get(url, params=params)
    results = r.json()['results']

    print results

    if len(results)>0:
        location = results[0]['geometry']['location']
        return location['lat'], location['lng'], results[0]['geometry']['location_type'], results[0]['formatted_address'], results[0]['place_id'], results[0]['types'][0]
    else:
        print '::', address

        na = None
        while na not in ('y', 'n'):
            na = raw_input('do you want to check the address? (y/n)')
            print na, [na]

        if na == 'y':
            a2 = raw_input('insert the new address : ').decode('utf8')
            return geocode(a2, key)
        elif na == 'n':
            return None, None, None, None

