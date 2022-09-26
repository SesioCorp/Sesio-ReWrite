from datetime import datetime
from email.policy import HTTP
import http
from http.client import HTTPResponse
from unicodedata import category
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic import View
from django.views.generic.edit import UpdateView

from workorder.forms import WorkOrderStatusForm, WorkOrderForm, WorkOrderAssignForm, WorkOrderUpdateForm
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
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

FORMS = [
    ("LocationForm", LocationForm),
    ("WorkOrderForm", WorkOrderForm),
    ("WorkOrderStatusForm", WorkOrderStatusForm),
]

TEMPLATES = {
    "LocationForm": "location_form.html",
    "WorkOrderForm": "workorder_form.html",
    "WorkOrderStatusForm": "workorder_status_form.html",
}


class WorkOrderListView(ListView):
    model = WorkOrder
    template_name = "workorder_listview.html"

    def get_context_data(self, **kwargs):
        context = super(WorkOrderListView, self).get_context_data(**kwargs)
        assigned_workorders_queryset = WorkOrder.objects.filter(
            status="open", assigned_to=self.request.user
        )
        unassigned_workorders_queryset = WorkOrder.objects.filter(
            status="open", assigned_to=CustomUser.objects.get(is_dispatch=True)
        )
        context["assigned_workorders"] = WorkOrderFilter(
            self.request.GET, queryset=assigned_workorders_queryset
        )
        try:
            context["urgent_count"] = WorkOrder.objects.filter(
                assigned_to=self.request.user,
                status="open",
                priority=Priority.objects.get(Q(name__startswith="U")),
            ).count()
        except Priority.DoesNotExist:
            context["urgent_count"] = 0

        try:
            context["unassigned_urgent_count"] = WorkOrder.objects.filter(
                assigned_to=CustomUser.objects.get(is_dispatch=True),
                status="open",
                priority=Priority.objects.get(Q(name__startswith="U")),
            ).count()
        except Priority.DoesNotExist:
            context["unassigned_urgent_count"] = 0
        context["unassigned_workorders"] = WorkOrderFilter(
            self.request.GET, queryset=unassigned_workorders_queryset
        )
        return context


class WorkOrderWizardView(SessionWizardView):
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, "uploads")
    )
    form_list = FORMS

    def get_context_data(self, form, **kwargs):
        context = super(WorkOrderWizardView, self).get_context_data(form=form, **kwargs)

        if self.steps.current == "WorkOrderStatusForm":
            user = CustomUser.objects.filter(
                is_dispatch=False, is_superuser=False
            ).exclude(pk=self.request.user.pk)
            dispatch_user = CustomUser.objects.filter(
                is_dispatch=True, is_superuser=False
            ).first()
            context.update({"users": user})
            context.update({"dispatch_user": dispatch_user})

        return context

    def get_form_list(self):
        return self.form_list

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def process_step(self, form):
        return self.get_form_step_data(form)

    def done(self, form_list, form_dict, **kwargs):
        location_data = form_dict["LocationForm"]
        location_object = location_data.save()
        workorder_data = form_dict["WorkOrderForm"]
        workorder_status_data = form_dict["WorkOrderStatusForm"]
        category_object = Category.objects.get(id=workorder_data.instance.category_id)
        priority_object = Priority.objects.get(
            id=workorder_status_data.instance.priority_id
        )

        try:
            _device_id = workorder_data.instance.enter_device_id_manually

        except ObjectDoesNotExist:
            _device_id = []

        try:
            asset = Asset.objects.get(device_id=_device_id)

        except ObjectDoesNotExist:
            asset = []
        timespent = self.request.POST.get("WorkOrderStatusForm-timespent")
        if timespent == "":
            timespent = 0
        else:
            timespent = timespent
        workorder_status = self.request.POST.get("WorkOrderStatusForm-status")
        if workorder_status == "open":
            workorder = WorkOrder.objects.create(
                created_at=datetime.now(),
                facility=location_object.facility,
                location=location_object,
                category=category_object,
                brief_description=workorder_data.instance.brief_description,
                description=workorder_data.instance.description,
                status=workorder_status_data.instance.status,
                priority=priority_object,
                enter_device_id_manually=workorder_data.instance.enter_device_id_manually,
                assigned_to=CustomUser.objects.get(
                    id=int(self.request.POST.get("WorkOrderStatusForm-assigned_to"))
                ),
                timespent=int(timespent),
            )
        else:
            workorder = WorkOrder.objects.create(
                created_at=datetime.now(),
                facility=location_object.facility,
                location=location_object,
                category=category_object,
                brief_description=workorder_data.instance.brief_description,
                description=workorder_data.instance.description,
                status=workorder_status_data.instance.status,
                priority=priority_object,
                enter_device_id_manually=workorder_data.instance.enter_device_id_manually,
                timespent=int(timespent),
                completed_at=self.request.POST.get("WorkOrderStatusForm-completed_at"),
            )

        if asset == []:
            workorder.save()

        else:
            workorder.asset.add(asset)
            workorder.save()

        return HttpResponseRedirect("/")


class EnterDeviceIdView(View):
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax:
            try:
                asset = Asset.objects.get(
                    device_id=self.request.POST.get("enter_device_id_manually")
                ).asset_type.name
                context = {"assets": asset}
                return JsonResponse(context)

            except Asset.DoesNotExist:
                context = {"assets": None}
                return JsonResponse(context)

class WorkOrderDetailView(DetailView):
    model = WorkOrder
    template_name = "workorder_detail.html"

    def get_context_data(self, **kwargs):
        context = super(WorkOrderDetailView, self).get_context_data(**kwargs)
        context["workorder_location_form"] = LocationForm(
            instance = self.get_object().location
        )
        context["workorder_assign_form"] = WorkOrderAssignForm(initial=self.workorder_assign_data())
        return context

    def workorder_assign_data(self):
        if self.get_object().assigned_to:
            data = {
                "requester": self.get_object().assigned_to,
                "req_email": self.get_object().assigned_to.email,
                "req_phone_number": self.get_object().assigned_to.phone_number,
                "type": "default",
                "created_on": self.get_object().created_at
            } 
            return data

class WorkOrderUpdateView(UpdateView):
    model = WorkOrder
    form_class = WorkOrderUpdateForm
    template_name = "workorder_update_form.html"
    success_url = reverse_lazy("workorder:work_order_list")

    def get_context_data(self, **kwargs):
        context = super(WorkOrderUpdateView, self).get_context_data(**kwargs)
        users = CustomUser.objects.filter(
            is_dispatch=False, is_superuser=False
            ).exclude(pk=self.request.user.pk)
        context["users"] = users
        dispatch_user = CustomUser.objects.filter(is_dispatch=True).first()
        context["dispatch_user"] = dispatch_user
        return context