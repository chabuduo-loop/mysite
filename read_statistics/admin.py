from django.contrib import admin
from .models import ReadNum , ReadDetail


# Register your models here.
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
	list_display = ('read_num' , 'content_object')

@admin.register(ReadDetail)
class ReadDetail(admin.ModelAdmin):
	list_display = ('read_num' , 'date' , 'content_object')