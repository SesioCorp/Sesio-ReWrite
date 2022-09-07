from email.policy import HTTP
import http
from http.client import HTTPResponse
from unicodedata import category
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from workorder.forms import WorkOrderStatusForm, WorkOrderForm
from systemandfacility.forms import LocationForm
from .models import Category, WorkOrder, Priority
from .filters import WorkOrderFilter
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
import os
from django.core.exceptions import ObjectDoesNotExist
from users.models import CustomUser
from django.http import HttpResponseRedirect
from asset.models import Asset
from django.conf import settings

FORMS = [
    ("LocationForm", LocationForm),
    ("WorkOrderForm", WorkOrderForm),
    ("WorkOrderStatusForm", WorkOrderStatusForm)
]

TEMPLATES = {
    "LocationForm": "locationform.html",
    "WorkOrderForm": "workorder_form.html",
    "WorkOrderStatusForm": "workorder_status.html"
}


class Home(TemplateView):
    template_name = 'index.html'

class WorkOrderListView(ListView):
    model = WorkOrder
    template_name = "workorder_listview.html"

    def get_context_data(self, **kwargs):
        context = super(WorkOrderListView, self).get_context_data(**kwargs)
        assigned_workorders_queryset = WorkOrder.objects.filter(
            assigned_to__isnull = False
        )
        unassigned_workorders_queryset = WorkOrder.objects.filter(
            assigned_to__isnull = True
        )
        context["assigned_workorders"] = WorkOrderFilter(self.request.GET, queryset=assigned_workorders_queryset)

        context["unassigned_workorders"] = WorkOrderFilter(self.request.GET, queryset=unassigned_workorders_queryset)
        return context

class WorkOrderWizardView(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "uploads"))
    form_list = FORMS
    
    def get_context_data(self, form, **kwargs):
        context = super(WorkOrderWizardView, self).get_context_data(form=form, **kwargs)
        if self.steps.current == "WorkOrderForm":
            user = CustomUser.objects.filter(is_dispatch=False, is_superuser=False).exclude(pk=self.request.user.pk)
            dispatch_user = CustomUser.objects.filter(is_dispatch=True)
            context.update({"users": user})
            context.update({"dispatch_users": dispatch_user})
        return context

    def get_form_list(self):
        return self.form_list
    
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def process_step(self, form):
        return self.get_form_step_data(form)

    def done(self, form_list, form_dict,**kwargs):
        location_data = form_dict["LocationForm"]
        location_object = location_data.save()
        workorder_data = form_dict["WorkOrderForm"]
        workorder_status_data = form_dict["WorkOrderStatusForm"]
        category_object = Category.objects.get(id=workorder_data.instance.category_id)
        priority_object = Priority.objects.get(id=workorder_status_data.instance.priority_id)
        
        try:
            _device_id = (workorder_data.instance.enter_device_id_manually)

        except ObjectDoesNotExist:
            _device_id = []
        
        try:
            assets = Asset.objects.get(barcode=_device_id)
        
        except ObjectDoesNotExist:
            assets = []
        import pdb; pdb.set_trace()
        workorder = WorkOrder.objects.create(
            facility = location_object.facility,
            location = location_object,
            category = category_object,
            brief_description = workorder_data.instance.brief_description,
            description = workorder_data.instance.description,
            status = workorder_status_data.instance.status,
            priority = priority_object,
            enter_device_id_manually = workorder_data.instance.enter_device_id_manually,
            assigned_to = CustomUser.objects.get(id=int(self.request.POST.get("WorkOrderStatusForm-assigned_to"))),
            timespent = int(self.request.POST.get('WorkOrderStatusForm-timespent'))
        )

        if assets == []:
            workorder.save()

        else:
            workorder.assets.add(assets)
            workorder.save()

        return HttpResponseRedirect("/")


