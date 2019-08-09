from django.urls import path
from . import views

app_name='pmos'

urlpatterns = [
    path('monitor/', views.monitor, name='monitor'),
    path('memo/', views.memo, name='memo'),
    path('memo_add/', views.memo_add, name='memo_add'),
    path('household/', views.household, name='household'),
    path('household_add/', views.household_add, name='household_add'),
]
