from django.shortcuts import render
from django.views.generic import TemplateView
from workorder.models import WorkOrder
from users.models import CustomUser

class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = WorkOrder.objects.all()
        assigned_wo = queryset.filter(status="open", assigned_to = self.request.user).count()
        context["work_order_count"] = assigned_wo
        return context


