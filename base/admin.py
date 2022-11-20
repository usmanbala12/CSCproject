from django.contrib import admin
from .models import Bus, Ticket

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Bus)