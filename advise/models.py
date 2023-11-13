from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Flag(models.Model):
    user = models.ForeignKey(to = User, on_delete = models.CASCADE)
    my_flag = models.BooleanField(default=False)

    def __str__(self):
        name = str(self.user.first_name) + str(self.user.last_name)
        return name
    
    class Meta:
        verbose_name_plural = 'Advice Comments'

class Student_Flag(models.Model):
    user = models.ForeignKey(to = User, on_delete = models.CASCADE)
    my_advice = models.BooleanField(default=False)

    def __str__(self):
        name = str(self.user.first_name) + str(self.user.last_name)
        return name