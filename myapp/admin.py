from django.contrib import admin
from .models import Event, Fight, Fighters, CareerStats, StrikeStats, FightPerformance, StrikeBreakdown, RoundStats


# Register your models here.
admin.site.register(Event)
admin.site.register(Fight)
admin.site.register(Fighters)
admin.site.register(CareerStats)
admin.site.register(StrikeStats)
admin.site.register(FightPerformance)
admin.site.register(StrikeBreakdown)
admin.site.register(RoundStats)