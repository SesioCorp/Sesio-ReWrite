from django.urls import path
from .views import Home, WorkOrderListView, WorkOrderWizardView

from systemandfacility.forms import LocationForm
from workorder.forms import WorkOrderForm, WorkOrderStatusForm

Forms = [
    ("LocationForm", LocationForm),
    ("WorkOrderForm", WorkOrderForm),
    ("WorkOrderStatusForm", WorkOrderStatusForm)    
]

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('workorder/', WorkOrderListView.as_view(), name='work_order_list'),
    path("create/", WorkOrderWizardView.as_view(Forms), name='work_order_create')
]