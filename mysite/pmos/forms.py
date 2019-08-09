import datetime
from django import forms
from .models import Memocond

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memocond
        fields = ('text',)
