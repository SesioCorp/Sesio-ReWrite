from django.shortcuts import render
from django.views.generic import TemplateView
from workorder.models import WorkOrder, Priority
from django.db.models import Q

class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = WorkOrder.objects.all()
        assigned_wo = queryset.filter(status="open", assigned_to = self.request.user).count()
        
        urgent_assigned_wo = queryset.filter(
            assigned_to=self.request.user,
            status="open",
            priority=Priority.objects.get(Q(name__startswith="U")))
        
        context["work_order_count"] = assigned_wo
        context["urgent_assigned_wo"] = urgent_assigned_wo
        return context



        