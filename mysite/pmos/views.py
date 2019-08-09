from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

import requests

from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse

from django.core import serializers

from pmos.models import Roomcond, Memocond, Housecond

from .forms import HouseForm, MemoForm
# Create your views here.

def monitor(request):
    roomcond_list = Roomcond.objects.all().order_by('-date')[:30]
    latest_roomcond = roomcond_list[0]
    return render(request, 'pmos/monitor.html', {'latest_roomcond':latest_roomcond})

def memo(request):
    memocond_list = Memocond.objects.all().order_by('-date')
    return render(request, 'pmos/memo.html', {'memocond_list':memocond_list})

def memo_add(request):
    if request.method == "POST":
        form = MemoForm(request.POST, request.FILES)
        if form.is_valid():
            memo = form.save(commit=False)
            url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=19c6ecde75f00332ef1416854a8fd1be'.format(memo.lat, memo.lon)
            url2 = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={}&y={}&input_coord=WGS84'.format(memo.lon, memo.lat)
            headers = {'Authorization':'KakaoAK ef023e151052064467c31652f247eae2'}
            city_name = requests.get(url2, headers=headers).json()
            city_weather = requests.get(url).json()
            weather={
                'city' : city_weather['name'],
                'temperature' : (round(city_weather['main']['temp']/10)),
                'humidity' : city_weather['main']['humidity'],
                'description' : city_weather['weather'][0]['description'],
            }
            memo.temp = weather['temperature']
            memo.humi = weather['humidity']
            memo.locate = city_name['documents'][0]['address_name']
            memo.weat = weather['description']
            memo.save()
            return HttpResponseRedirect(reverse('pmos:memo')) # Redirect after POST
    else:
        form = MemoForm()
        return render(request, 'pmos/memo_add.html', {'form':form})

#def memo_reg(request, Memocond_id):
#    memocond = get_object_or_404(Memocond, pk=Memocond_id)
#    memocond.save()
#    return HttpResponseRedirect(reverse('pmos:memo'))

def household(request):
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
            return HttpResponseRedirect(reverse('pmos:household')) # Redirect after POST
    else:
        form = HouseForm()
        household_list = Housecond.objects.all().order_by('-id')
        prev_housecond = household_list[0]
        return render(request, 'pmos/household_add.html', {'form':form, 'prev_housecond':prev_housecond})
