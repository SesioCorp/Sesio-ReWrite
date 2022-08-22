from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import WorkOrder


class Home(TemplateView):
    template_name = 'index.html'

class WorkOrderListView(ListView):
    model = WorkOrder
    template_name = "workorder_listview.html"