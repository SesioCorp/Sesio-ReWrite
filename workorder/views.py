from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import WorkOrder
from .filters import WorkOrderFilter


class Home(TemplateView):
    template_name = 'index.html'

class WorkOrderListView(ListView):
    model = WorkOrder
    template_name = "workorder_listview.html"

    def get_context_data(self, **kwargs):
        context = super(WorkOrderListView, self).get_context_data(**kwargs)
        assigned_workorders_queryset = WorkOrder.objects.filter(
            assigned__isnull = False
        )
        unassigned_workorders_queryset = WorkOrder.objects.filter(
            assigned__isnull = True
        )
        context["assigned_workorders"] = WorkOrderFilter(self.request.GET, queryset=assigned_workorders_queryset)

        context["unassigned_workorders"] = WorkOrderFilter(self.request.GET, queryset=unassigned_workorders_queryset)
        return context