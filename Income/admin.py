from django.contrib import admin
from .models import Income, Source

admin.site.register(Source)
admin.site.register(Income)