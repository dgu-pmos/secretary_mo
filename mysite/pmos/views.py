from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

import requests

from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse

from django.core import serializers

from pmos.models import Roomcond, Memocond, Housecond

from .forms import HouseForm
# Create your views here.

def monitor(request):
    roomcond_list = Roomcond.objects.all().order_by('-date')[:30]
    latest_roomcond = roomcond_list[0]
    return render(request, 'pmos/monitor.html', {'latest_roomcond':latest_roomcond})

def memo(request):
    memocond_list = Memocond.objects.all().order_by('-date')
    url = 'http://api.openweathermap.org/data/2.5/weather?lat=37.5400399&lon=127.09341909999999&appid=19c6ecde75f00332ef1416854a8fd1be'
    #url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=19c6ecde75f00332ef1416854a8fd1be'
    city = 'Seoul'
    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
    weather={
    'city' : city,
    'temperature' : city_weather['main']['temp'],
    'description' : city_weather['weather'][0]['description'],
    }
    return render(request, 'pmos/memo.html', {'memocond_list':memocond_list, 'weather':weather})

#def memo_reg(request, Memocond_id):
#    memocond = get_object_or_404(Memocond, pk=Memocond_id)
#    memocond.save()
#    return HttpResponseRedirect(reverse('pmos:memo'))

def household_view(request):
    household_list = Housecond.objects.filter(date__month='8')
    return render(request, 'pmos/household.html', {'household_list':household_list})

def household_add(request):
    if request.method == "POST":
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            house = form.save(commit=False)
            if house.use == "이체":
                house.balance = house.balance + house.expense
            else :
                house.balance = house.balance - house.expense
            house.save()
            return HttpResponseRedirect(reverse('pmos:household_view')) # Redirect after POST
    else:
        form = HouseForm()
        household_list = Housecond.objects.all().order_by('-id')
        prev_housecond = household_list[0]
        return render(request, 'pmos/household_add.html', {'form':form, 'prev_housecond':prev_housecond})
