from django.contrib import admin
from django.urls import path, include
from django.contrib import admin

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('dashboard.urls', 'dashboard'), namespace="dashboard")),
    path('workorder/', include(('workorder.urls', 'workorder'), namespace="workorder")),
    path('systemandfacility/', include(('systemandfacility.urls', 'systemandfacility'), namespace="systemandfacility"))
]
