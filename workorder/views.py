from datetime import datetime
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

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


class WorkOrderListView(LoginRequiredMixin, ListView):
    model = WorkOrder

    def get_assigned_workorders(self):
        assigned_workorders_queryset = WorkOrder.objects.filter(
            status="open", assigned_to=self.request.user
        )
        return assigned_workorders_queryset
    
    def get_unassigned_workorders(self):
        unassigned_workorders_queryset = WorkOrder.objects.filter(
            status="open", assigned_to=CustomUser.objects.get(is_dispatch=True)
        )
        return unassigned_workorders_queryset

    def get_urgent_priority(self):
        urgent_priority=Priority.objects.get(Q(name__startswith="U"))
        return urgent_priority

    def get_assigned_workorders_urgent_count(self):
        assigned_workorders_urgent_count = self.get_assigned_workorders().filter(
                priority=self.get_urgent_priority(),
            ).count()
        return assigned_workorders_urgent_count

    def get_unassigned_workorders_urgent_count(self):
        unassigned_workorders_urgent_count = self.get_unassigned_workorders().filter(
                priority=self.get_urgent_priority(),
            ).count()
        return unassigned_workorders_urgent_count

    def get_context_data(self, **kwargs):
        context = super(WorkOrderListView, self).get_context_data(**kwargs)
        context["assigned_workorders"] = WorkOrderFilter(
            self.request.GET, queryset=self.get_assigned_workorders()
        )
        context["unassigned_workorders"] = WorkOrderFilter(
            self.request.GET, queryset=self.get_unassigned_workorders()
        )
        try:
            context["assigned_workorders_urgent_count"] = self.get_assigned_workorders_urgent_count()
        except Priority.DoesNotExist:
            context["assigned_workorders_urgent_count"] = 0

        try:
            context["unassigned_workorders_urgent_count"] = self.get_unassigned_workorders_urgent_count()
        except Priority.DoesNotExist:
            context["unassigned_workorders_urgent_count"] = 0

        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return 'partials/dropdown_list.html'
        return 'workorder_listview.html'

class WorkOrderWizardView(LoginRequiredMixin, SessionWizardView):
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, "uploads")
    )
    form_list = FORMS

    def get_users(self):
        users = CustomUser.objects.filter(
                is_dispatch=False, is_superuser=False
            ).exclude(pk=self.request.user.pk)
        return users

    def get_dispatch_user(self):
        dispatch_user = CustomUser.objects.filter(
                is_dispatch=True, is_superuser=False
            ).first()
        return dispatch_user

    def get_context_data(self, form, **kwargs):
        context = super(WorkOrderWizardView, self).get_context_data(form=form, **kwargs)

        if self.steps.current == "WorkOrderStatusForm":
            users = self.get_users()
            dispatch_user = self.get_dispatch_user()
            context.update({"users": users})
            context.update({"dispatch_user": dispatch_user})

        return context

    def get_form_list(self):
        return self.form_list

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def process_step(self, form):
        return self.get_form_step_data(form)

    def get_time_spent(self):
        time_spent = self.request.POST.get("WorkOrderStatusForm-timespent")
        if time_spent == "":
            time_spent = 0
        else:
            time_spent = time_spent
        return time_spent

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

        time_spent = self.get_time_spent()

        workorder_status = self.request.POST.get("WorkOrderStatusForm-status")
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
            timespent=int(time_spent),
        )   
        

        if workorder_status == "open":
            workorder.assigned_to = CustomUser.objects.get(
                id=int(self.request.POST.get("WorkOrderStatusForm-assigned_to"))
            )
            workorder.save()

        else:
            workorder.completed_at = self.request.POST.get("WorkOrderStatusForm-completed_at")
            workorder.save()

        if asset == []:
            workorder.save()

        else:
            workorder.asset.add(asset)
            workorder.save()

        return HttpResponseRedirect("/")


class EnterDeviceIdView(LoginRequiredMixin, View):
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


class WorkOrderDetailView(LoginRequiredMixin, DetailView):
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

    def post(self, request, *args, **kwargs):
        location_form = LocationForm(self.request.POST)
        workorder_assigned_form = WorkOrderAssignForm(self.request.POST)
        object_data = self.get_object()

        if location_form.is_valid():
            object_data.facility = location_form.cleaned_data['facility']
            object_data.location.building = location_form.cleaned_data['building']
            object_data.location.floor = location_form.cleaned_data['floor']
            object_data.location.department = location_form.cleaned_data['department']
            object_data.location.specific_location = location_form.cleaned_data['specific_location']
            object_data.facility.save()
            object_data.location.save()
            object_data.save()

        if not workorder_assigned_form.data['requester']:
            object_data.save()

        else:
            object_data.assigned_to = CustomUser.objects.get(pk=int(workorder_assigned_form.data['requester']))
            object_data.save()

        return HttpResponseRedirect(reverse("workorder:work_order_update", kwargs={"pk":self.get_object().pk}))

class WorkOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkOrder
    form_class = WorkOrderUpdateForm
    template_name = "workorder_update_form.html"
    success_url = reverse_lazy("workorder:work_order_list")

    def get_users(self):
        users = CustomUser.objects.filter(
                is_dispatch=False, is_superuser=False
            ).exclude(pk=self.request.user.pk)
        return users

    def get_dispatch_user(self):
        dispatch_user = CustomUser.objects.filter(
                is_dispatch=True, is_superuser=False
            ).first()
        return dispatch_user

    def get_context_data(self, **kwargs):
        context = super(WorkOrderUpdateView, self).get_context_data(**kwargs)
        users = self.get_users()
        dispatch_user = self.get_dispatch_user()
        context["users"] = users
        context["dispatch_user"] = dispatch_user
        return context