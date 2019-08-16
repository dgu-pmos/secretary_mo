from django.contrib import admin

from pmos.models import Roomcond, Memocond, Housecond, Balance
# Register your models here.

admin.site.register(Roomcond)
admin.site.register(Memocond)
admin.site.register(Housecond)
admin.site.register(Balance)
