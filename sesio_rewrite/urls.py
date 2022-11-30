from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('dashboard.urls', 'dashboard'), namespace="dashboard")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('workorder/', include(('workorder.urls', 'workorder'), namespace="workorder")),
    path('systemandfacility/', include(('systemandfacility.urls', 'systemandfacility'), namespace="systemandfacility")),
    path('preventivemaintenance/', include(('preventivemaintenance.urls', 'preventivemaintenance'), namespace="preventivemaintenance")),
    path('question/', include(('question.urls', 'question'), namespace='question'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)