import datetime
from django import forms
from .models import Memocond, Housecond

class HouseForm(forms.ModelForm):
    class Meta:
        model = Housecond
        fields=('balance', 'expense', 'person', 'use', 'comment', 'date')

        #balance = forms.IntegerField(initial = prev_housecond.balance)
        #expense = forms.IntegerField()
        #person = forms.CharField()
        #use = forms.CharField()
        #comment = forms.CharField()
        #date = forms.DateField(initial=datetime.date.today)
