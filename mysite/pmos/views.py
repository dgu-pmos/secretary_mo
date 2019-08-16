from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect

import requests, json

from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse

from pmos.models import Roomcond, Memocond, Housecond, Balance

from .forms import RoomForm, HouseForm, MemoForm

from django.contrib.auth import get_user

import datetime

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

headers = {'Authorization':'KakaoAK ef023e151052064467c31652f247eae2'}

def monitor(request):
    roomcond_list = Roomcond.objects.all().order_by('-id')[:20]
    latest_roomcond = roomcond_list[0]
    return render(request, 'pmos/monitor.html', {'latest_roomcond':latest_roomcond})

def memo(request):
    memocond_list = Memocond.objects.all().order_by('-date')[:20]
    return render(request, 'pmos/memo.html', {'memocond_list':memocond_list})

def memo_add(request):
    if request.method == "POST":
        form = MemoForm(request.POST, request.FILES)
        if form.is_valid():
            memo = form.save(commit=False)
            url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=19c6ecde75f00332ef1416854a8fd1be'.format(memo.lat, memo.lon)
            url2 = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={}&y={}&input_coord=WGS84'.format(memo.lon, memo.lat)
            city_name = requests.get(url2, headers=headers).json()
            city_weather = requests.get(url).json()
            memo.temp = round(city_weather['main']['temp']/10)
            memo.humi = city_weather['main']['humidity']
            memo.locate = city_name['documents'][0]['address_name']
            memo.weat = city_weather['weather'][0]['description']
            memo.save()
            return HttpResponseRedirect(reverse('pmos:memo')) # Redirect after POST
    else:
        form = MemoForm()
        return render(request, 'pmos/memo_add.html', {'form':form})

def memo_edit(request, memocond_id):
    memo = Memocond.objects.get(id=memocond_id)
    if request.method == "POST":
        form = MemoForm(request.POST, request.FILES)
        if form.is_valid():
            memo.text = form.cleaned_data['text']
            memo.lat = form.cleaned_data['lat']
            memo.lon = form.cleaned_data['lon']
            url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=19c6ecde75f00332ef1416854a8fd1be'.format(memo.lat, memo.lon)
            url2 = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={}&y={}&input_coord=WGS84'.format(memo.lon, memo.lat)
            city_name = requests.get(url2, headers=headers).json()
            city_weather = requests.get(url).json()
            memo.temp = round(city_weather['main']['temp']/10)
            memo.humi = city_weather['main']['humidity']
            memo.locate = city_name['documents'][0]['address_name']
            memo.weat = city_weather['weather'][0]['description']
            memo.save()
            return HttpResponseRedirect(reverse('pmos:memo')) # Redirect after POST
    else:
        form = MemoForm()
        return render(request, 'pmos/memo_edit.html', {'form':form})

def memo_delete(request, memocond_id):
    obj = Memocond.objects.get(pk=memocond_id)
    obj.delete()
    return redirect('/pmos/memo')

def household_main(request):
    household_balance = Balance.objects.get(pk=1)
    household_list = Housecond.objects.all()
    for housecond in household_list:
        if housecond.use == '이체':
            household_balance.new_balance += housecond.expense
        else :
            household_balance.new_balance -= housecond.expense
    return render(request, 'pmos/household_main.html', {'household_balance':household_balance})

def household(request):
    household_list = Housecond.objects.filter(date__month=datetime.date.today().month)
    return render(request, 'pmos/household.html', {'household_list':household_list})

def household_add(request):
    if request.method == "POST":
        current_user=get_user(request)
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            house = form.save(commit=False)
            house.person = current_user.first_name
            house.save()
            return HttpResponseRedirect(reverse('pmos:household_main')) # Redirect after POST
    else:
        form = HouseForm()
        return render(request, 'pmos/household_add.html', {'form':form})

def household_edit(request, housecond_id):
    house = Housecond.objects.get(id=housecond_id)
    if request.method=='POST':
        current_user=get_user(request)
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            house.expense = form.cleaned_data['expense']
            house.person = current_user.first_name
            house.use = form.cleaned_data['use']
            house.comment = form.cleaned_data['comment']
            house.save()
            return HttpResponseRedirect(reverse('pmos:household_main'))
    else:
        form = HouseForm()
        return render(request, 'pmos/household_edit.html', {'form':form})

def household_delete(request, housecond_id):
    obj = Housecond.objects.get(pk=housecond_id)
    obj.delete()
    return redirect('/pmos/household_main')

@csrf_exempt
def room_add(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        new_roomcond = Roomcond(temp = received_json_data['temp'], humi = received_json_data['humi'])
        new_roomcond.save()
        return HttpResponse('ok')
