from dotenv import load_dotenv
import os
import requests
import pprint
from flask import abort

pp = pprint.PrettyPrinter(width=41, compact=True)

def get_geocode(address):
    if address is None or address.strip() is "":
        abort(400, "Invalid address")

    p = {'q': address, 'api_key': os.environ.get("geocode-key")}
    res = requests.get('https://api.geocod.io/v1.6/geocode', params=p)

    # check if api gives invalid response
    if res.status_code == 200:
        # parse data as json and retrieve lat and long
        data = res.json()
        # pp.pprint(data)
        if data['results']:
            lat = data['results'][0]['location']['lat']
            lng = data['results'][0]['location']['lng']
        else:
            abort(400, "Invalid address")
    else:
        abort(500, "Geocod.io Unavailable to Process Request")
    
    return lat, lng

def find_food(lat, lng):
    p = {'latitude': lat, 'longitude': lng, 'categories': 'Food'}
    h = {'Authorization': 'Bearer {}'.format(os.environ.get("yelp-key"))}
    res = requests.get('https://api.yelp.com/v3/businesses/search', params=p, headers=h)

    # check if api gives invalid response
    if res.status_code == 200:
        # parse our response and return
        data = res.json()
        business_info = []
        for b in data['businesses']:
            business_info.append({'name': b['name'], 'address': ' '.join(b['location']['display_address']), 'rating': b['rating']})
        return business_info
    else:
        abort(500, "Yelp Service Unavailable")
