from django.contrib import admin
from .models import Chart, CSVFile, Dashboard
# from django.contrib.admin.decorators import ad
# Register your models here.

admin.site.register(Chart)
admin.site.register(CSVFile)
admin.site.register(Dashboard)