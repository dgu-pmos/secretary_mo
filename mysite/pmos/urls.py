from django.urls import path
from . import views

app_name='pmos'

urlpatterns = [
    path('monitor/', views.monitor, name='monitor'),
    path('memo/', views.memo, name='memo'),
    path('memo_add/', views.memo_add, name='memo_add'),
    path('memo_edit/<int:memocond_id>/', views.memo_edit, name='memo_edit'),
    path('memo_delete/<int:memocond_id>/', views.memo_delete, name='memo_delete'),
    path('household/', views.household, name='household'),
    path('household_add/', views.household_add, name='household_add'),
    path('household_main/', views.household_main, name='household_main'),
    path('household_edit/<int:housecond_id>/', views.household_edit, name='household_edit'),
    path('household_delete/<int:housecond_id>/', views.household_delete, name='household_delete'),
    path('room_add/', views.room_add, name='room_add')
]
