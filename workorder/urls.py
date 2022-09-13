from django.urls import path
from .views import WorkOrderListView, WorkOrderWizardView, EnterDeviceIdView

from systemandfacility.forms import LocationForm
from workorder.forms import WorkOrderForm, WorkOrderStatusForm

Forms = [
    ("LocationForm", LocationForm),
    ("WorkOrderForm", WorkOrderForm),
    ("WorkOrderStatusForm", WorkOrderStatusForm)    
]

urlpatterns = [
    path('list/', WorkOrderListView.as_view(), name='work_order_list'),
    path("new/", WorkOrderWizardView.as_view(Forms), name='work_order_create'),
    path("enterdevice/", EnterDeviceIdView.as_view(), name='enter_device')
]