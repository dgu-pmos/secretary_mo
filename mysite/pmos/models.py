from django.db import models
from datetime import datetime

class Roomcond(models.Model):
    temp = models.IntegerField(default=0)
    humi = models.IntegerField(default=0)
    motion = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "temp : {}, humi : {}, motion : {}".format(self.temp,self.humi,self.motion)

class Memocond(models.Model):
    text = models.CharField(max_length = 100)
    gps = models.CharField(max_length = 50)
    weat = models.CharField(max_length = 10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Housecond(models.Model):
    balance = models.IntegerField()
    expense = models.IntegerField()
    person = models.CharField(max_length=10)
    use = models.CharField(max_length=20)
    comment = models.CharField(max_length=50)
    date = models.DateField(default=datetime.today)
