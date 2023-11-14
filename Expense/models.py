from django.db import models
from django.utils.timezone import now, localtime
from django.contrib.auth.models import User
from Income.models import Source

# Create your models here.


class Category(models.Model):
    user = models.ForeignKey(to = User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 256)
    created_at = models.DateTimeField(default=localtime)

    def __str__(self):
        return str(self.user) + self.name
    
    class Meta:
        verbose_name_plural = 'Expense Categories'


# expense model
class Expense(models.Model):
    user = models.ForeignKey(to = User,on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField(default = localtime)
    description = models.TextField()
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE)
    source = models.ForeignKey(to = Source, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=localtime)
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.title) + str(self.category) + str(self.date )+ str(self.amount)

    class Meta:
        ordering:['-date']


