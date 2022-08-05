from django.contrib import admin
from .models import AssetAttributeSet, AssetType, Asset
# Register your models here.

admin.site.register(AssetAttributeSet)
admin.site.register(AssetType)
admin.site.register(Asset)