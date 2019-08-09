from django.urls import path
from . import views

app_name='pmos'

urlpatterns = [
    path('monitor/', views.monitor, name='monitor'),
    path('memo/', views.memo, name='memo'),
    path('memo_add/', views.memo_add, name='memo_add'),
    path('household/', views.household_view, name='household_view'),
    path('household/', views.household_add, name='household_add'),
    #path('<int:Memocond_id>/vote/', views.memo_reg, name='memo_reg'),
    #path('check/', views.check, name='check'),
    #path('main/', views.detail, name='main'),
]
