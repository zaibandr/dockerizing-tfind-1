from django.contrib import admin

# Register your models here.
from .models import Torrent, Trend


admin.site.register(Torrent)
admin.site.register(Trend)
