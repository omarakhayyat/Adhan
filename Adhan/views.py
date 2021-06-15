import datetime
import os
from datetime import datetime
from time import strptime

import geoip2.database
import geoip2
import pytz
from django.shortcuts import render
from django.utils.datetime_safe import date
from opencage.geocoder import OpenCageGeocode
from Adhan.prayertimes import prayTimes


def index(request):
    return render(request, 'index.html')


def showtiming(request):
    key = '83a5bb95eb4a401d8bec90ffcd934157'
    if request.method == 'POST' and request.POST.get('ip') is not None:
        ipaddress = request.POST.get('ip')

        reader = geoip2.database.Reader('Adhan/static/GeoLite2-City.mmdb')
        response = reader.city(ipaddress)
        reader.close()

        ist = pytz.timezone(response.location.time_zone)
        local_datetime = ist.localize(datetime.now())

        times = prayTimes.getTimes(date.today(), (response.location.latitude, response.location.longitude),
                                   int(local_datetime.strftime('%Z')))
        return render(request, 'adhan.html', {'times': times})

    elif request.method == 'POST' and request.POST.get('city') is not None:
        city = request.POST.get('city')
        geocoder = OpenCageGeocode(key)
        results = geocoder.geocode(city)
        time_zone = int(results[0]['annotations']['timezone']['offset_string'][:3])
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']

        times = prayTimes.getTimes(strptime(request.POST.get('date'), '%Y-%m-%d'), (latitude, longitude), time_zone)

        return render(request, 'adhan.html', {'times': times})
    else:
        return render(request, 'adhan.html')


