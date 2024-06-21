from django.contrib import admin
from home.models import UserDailyStats, UserStaticStats, UserGoals, UserMood

admin.site.register(UserDailyStats)
admin.site.register(UserStaticStats)
admin.site.register(UserGoals)
admin.site.register(UserMood)

