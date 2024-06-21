from django.contrib import admin
from home.models import UserDailyStats, UserStaticStats, UserGoals

admin.site.register(UserDailyStats)
admin.site.register(UserStaticStats)
admin.site.register(UserGoals)
