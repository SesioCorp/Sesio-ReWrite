from django.contrib import admin
from .models import Category, Priority, WorkOrder, Comment, TimeSpent
# Register your models here.

admin.site.register(Category)
admin.site.register(Priority)
admin.site.register(WorkOrder)
admin.site.register(Comment)
admin.site.register(TimeSpent)