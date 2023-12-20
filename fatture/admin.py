from django.contrib import admin

from fatture.models import Fattura, Cliente, Viaggio

# Register your models here.

admin.site.register(Fattura)
admin.site.register(Cliente)
admin.site.register(Viaggio)