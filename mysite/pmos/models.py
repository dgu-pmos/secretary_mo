from django.db import models
from datetime import datetime
from django.utils import timezone

class Roomcond(models.Model):
    temp = models.IntegerField(default=0)
    humi = models.IntegerField(default=0)
    motion = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "temp : {}, humi : {}, motion : {}".format(self.temp,self.humi,self.motion)

class Memocond(models.Model):
    text = models.CharField(max_length = 100)
    lat = models.FloatField(max_length = 100, default=37.5400399)
    lon = models.FloatField(max_length = 100, default=127.09341909999999)
    locate = models.CharField(max_length = 50, default='aa')
    temp = models.IntegerField(default=30)
    humi = models. IntegerField(default=30)
    weat = models.CharField(max_length = 20, default='bb')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Housecond(models.Model):
    expense = models.IntegerField()
    person = models.CharField(max_length=20)
    use = models.CharField(max_length=20)
    comment = models.CharField(max_length=50, default='-')
    date = models.DateTimeField(auto_now_add=True)

class Balance(models.Model):
    new_balance = models.IntegerField(default=0)
