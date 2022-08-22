from django.urls import path
from .views import Home, WorkOrderListView


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('workorder/', WorkOrderListView.as_view(), name='work_order_list'),
]