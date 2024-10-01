from django.db import models
from stats.constants import GENDER_CHOICES
from django.contrib.auth.models import User
from django.utils import timezone


class UserPhysicalData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.IntegerField(blank=False)
    weight = models.IntegerField(blank=False)
    age = models.IntegerField(blank=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
    

class UserDailyStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.IntegerField(default=0)
    water = models.IntegerField(default=0)
    active = models.IntegerField(default=0)
    kcal = models.IntegerField(default=0)
    sleep = models.TimeField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} | {self.date}"
    
class UserGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.IntegerField()
    water = models.IntegerField()
    active = models.IntegerField()
    kcal = models.IntegerField()
    sleep = models.TimeField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} | {self.date}"

