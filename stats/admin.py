from django.contrib import admin
from stats.models import *

admin.site.register(UserPhysicalData)
admin.site.register(UserDailyStats)
admin.site.register(UserGoals)