from django.contrib import admin
from .models import Fighter, FighterStats, Bout

# Register your models here.
admin.site.register(Fighter)
admin.site.register(FighterStats)
admin.site.register(Bout)