from django.contrib import admin
from .models import Flag, Student_Flag
# register Flag, Student_Flag class from advice.models to admin site

admin.site.register(Flag)
admin.site.register(Student_Flag)