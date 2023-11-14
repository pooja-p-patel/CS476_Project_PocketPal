from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime, now


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(to = User,on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    body = models.TextField()
    student_name = models.CharField(max_length=100)
    created_on = models.DateTimeField(default=now)

# Observerlist added
class Observer(models.Model):
    user = models.ForeignKey(to = User,on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.user.first_name) + str(self.user.last_name)
        return name