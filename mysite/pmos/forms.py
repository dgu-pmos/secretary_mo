import datetime
from django import forms
from .models import Roomcond, Memocond, Housecond

class HouseForm(forms.ModelForm):
    class Meta:
        model = Housecond
        fields=('expense', 'use', 'comment')

        #balance = forms.IntegerField(initial = prev_housecond.balance)
        #expense = forms.IntegerField()
        #person = forms.CharField()
        #use = forms.CharField()
        #comment = forms.CharField()
        #date = forms.DateField(initial=datetime.date.today)

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memocond
        fields=('text', 'lat', 'lon',)
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Roomcond
        fields=('temp', 'humi', 'motion',)
