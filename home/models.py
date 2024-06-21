from django.db import models

# Create your models here.
class UserStaticStats(models.Model):
    username = models.CharField(max_length=50)
    data = models.JSONField(default=list)

    def __str__(self):
        return self.username

class UserDailyStats(models.Model):
    username = models.CharField(max_length=50)
    data = models.JSONField(default=dict)

    def __str__(self):
        return self.username

class UserGoals(models.Model):
    username = models.CharField(max_length=50)
    data = models.JSONField(default=list)
    
    def __str__(self):
        return self.username
    
class UserMood(models.Model):
    username = models.CharField(max_length=50)
    data = models.JSONField(default=dict)
    
    def __str__(self):
        return self.username


