from django.urls import reverse
from django.shortcuts import render
from .models import PreventiveMaintenance
from .filters import PreventiveMaintenanceFilter
from django.views.generic.list import ListView
from django.views.generic import DetailView, View
from systemandfacility.forms import LocationForm
from .forms import PreventiveMaintenanceAssetDetailsForm
from asset.models import *
from django.http import HttpResponseRedirect
from .questionanswerform import PreventiveMaintenanceQuestionAnswerForm
from django.contrib import messages
from django.shortcuts import redirect, render


TEXT = "text"
SHORT_TEXT = "short_text"
RADIO = "radio"
SELECT = "select"
SELECT_IMAGE = "select_image"
SELECT_MULTIPLE = "select_multiple"
INTEGER = "integer"
FLOAT = "float"
DATE = "date"


class PreventiveMaintenanceListView(ListView):
   
    model = PreventiveMaintenance
   
    def get_queryset(self):

        if self.request.is_ajax():
            queryset = self.model.objects.all()
            filtered_queryset = PreventiveMaintenanceFilter(self.request.GET, queryset=queryset)
            return filtered_queryset.qs

        queryset = self.model.objects.all()
        filtered_queryset = PreventiveMaintenanceFilter(self.request.GET, queryset=queryset)
        return filtered_queryset

    def get_template_names(self):
        if self.request.is_ajax():
            return 'preventivemaintenance/partials/dropdown_list.html'
        return 'preventivemaintenance_listview.html'

class PreventiveMaintenanceDetailView(DetailView):
    model = PreventiveMaintenance
    template_name = "preventivemaintenance_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PreventiveMaintenanceDetailView, self).get_context_data(**kwargs)
        context["location_form"] = LocationForm(instance=self.get_object().asset.location)
        context["asset_update"] = PreventiveMaintenanceAssetDetailsForm(initial=self.pm_asset_details())
        return context

    def pm_asset_details(self):
        try:
            data = {
                "asset_type": self.get_object().asset.asset_type,
                "weight": self.get_object().asset.attribute_set.weight,
                "brand": self.get_object().asset.attribute_set.brand
            }

        except Asset.DoesNotExist: 
            data = {
                "asset_type": None,
                "weight": None,
                "brand": None
            }

        return data

    def post(self, request, *args, **kwargs):
        location_form = LocationForm(self.request.POST)
        asset_form = PreventiveMaintenanceAssetDetailsForm(self.request.POST)

        if location_form.is_valid():
            object_data = self.get_object()
            if object_data.asset.location:
                object_data.facility = location_form.cleaned_data['facility']
                object_data.asset.location.building = location_form.cleaned_data['building']
                object_data.asset.location.floor = location_form.cleaned_data['floor']
                object_data.asset.location.department = location_form.cleaned_data['department']
                object_data.asset.location.specific_location = location_form.cleaned_data['specific_location']
                object_data.asset.location.save()
                object_data.facility.save()
                object_data.save()
        
        if asset_form.is_valid():
            object_data = self.get_object()
            if object_data.asset:
                object_data.asset.asset_type = asset_form.cleaned_data['asset_type']
                object_data.asset.attribute_set.weight = asset_form.cleaned_data['weight']
                object_data.asset.attribute_set.brand = asset_form.cleaned_data['brand']
                object_data.asset.asset_type.save()
                object_data.asset.attribute_set.save()
                object_data.save()

        return HttpResponseRedirect(reverse("preventivemaintenance:preventive_maintenance_list"))


class PreventiveMaintenanceQuestionAnswerView(View):
    template_name = "preventivemaintenance_question_answer.html"

    def get(self, request, *args, **kwargs):
        asset = Asset.objects.get(pk=int(kwargs.get("pk")))
        step_number = kwargs.get("step", 0)
        question_step_number = kwargs.get("question_step", 0)
        slug = kwargs.get("slug", 0)
        preventivemaintenance = PreventiveMaintenance.objects.get(slug=slug)
        forms = PreventiveMaintenanceQuestionAnswerForm(
            slug=slug, asset=asset, user=request.user, step=step_number
        )
        categories = forms.categories
        comment_category = ""
        for category in categories:
            if category.is_comment:
                comment_category = category
        
        context = {
            "forms": forms,
            "categories": categories,
            "question_set": self.get_question_and_category_by_question_set(asset),
            "preventivemaintenance_slug": slug,
            "asset": asset,
            "pk": asset.pk,
            "preventivemaintenance": preventivemaintenance,
            "step": step_number,
            "question_step": question_step_number,
            "question_id": request.GET.get("question_id", 0),
            "kwargs": kwargs 
        }
        if request.is_ajax():
            try:
                parent_question = asset.question_set.question.get(
                    pk=request.GET.get("question_id", 0)
                )
                if parent_question.answer_type in [TEXT, SHORT_TEXT, INTEGER, FLOAT, DATE]:
                    child_question = parent_question.get_all_child_questions(include_self=False)[0]
                else:
                    child_question = asset.question_set.question.filter(
                        parent=parent_question.pk,
                        parent_answer__contains=request.GET.get("answer", 0)
                    ).get()
            except Exception:
                child_question = None
            
            ctx = {
                "question": child_question,
                "answer": self.get_answer_by_preventive_maintenance(child_question, preventivemaintenance),
                "slug": slug,
                "asset": asset,
                "question_set": self.get_question_and_categroy_by_question_set(asset),
                "comment_question_id": asset.question_set.question.filter(
                    parent=child_question, category__is_comment=True, deleted=True
                ).first().pk if asset.question_set.question.filter(
                    parent=child_question, category__is_comment=True, deleted=True
                ).exists() else "",
                "comment_catagory": comment_category,
                "preventivemaintenance": preventivemaintenance,
                "parent_question_text": child_question.parent.question_text if child_question and child_question.parent
                and len(child_question.parent.get_all_child_questions(include_self=False)) == 2 else "",
                "question_child_count": len(
                    child_question.get_all_child_questions(include_self=False)
                ) if child_question else "",
                "question_parent_child_count": len(
                    child_question.parent.get_all_child_questions(include_self=False)
                ) if child_question and child_question.parent else "",
                "child_questions": ",".join(
                    [
                        str(obj.pk) for obj in child_question.get_all_child_questions(include_self=False)
                    ]
                ) if child_question else "",
                "parent_question_ids": ",".join(
                    [
                        str(obj.pk) for obj in child_question.get_all_child_questions(include_self=False)
                    ]
                ) if child_question else "",
                "fail_condition_answer": child_question.parent_question.filter(
                    category=child_question.category
                ).first().parent_answer if child_question.parent_question.filter(
                    category=child_question.category
                ).exists() else ""
            }
            render_template = "preventivemaintenance/partials/form_render.html"
            return render(request, render_template, ctx)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        asset = Asset.objects.get(pk=int(kwargs.get("pk")))
        step = kwargs.get("step", 0)
        slug = kwargs.get("slug", 0)
        preventivemaintenance = PreventiveMaintenance.objects.get(slug=slug)
        save_and_exit = False
        forms = PreventiveMaintenanceQuestionAnswerForm(
            request.POST,
            request.FILES or None,
            slug=slug,
            asset=asset,
            user=request.user,
            step=step
        )
        categories = forms.current_categories
        context = {
            "forms": forms,
            "asset": asset,
            "categories": categories
        }

        if forms.is_valid():
            if save_and_exit:
                messages.warning(self.request, f"Status: {asset} in progress")
            else:
                messages.warning(self.request, f"Status: {asset} completed")
            return self.treat_valid_form(forms, kwargs, request, asset, preventivemaintenance)
        return self.handle_invalid_form(context, forms, request, asset)


    def get_question_and_category_by_question_set(self, asset):
        data = {}
        categories = asset.question_set.question.values("category").distinct()
        for category_id in categories:
            try:
                category = QuestionCategory.objects.get(pk=category_id["category"])
                data[category.title] = 0
            except Exception:
                category = category_id
                data[category["category"]] = 0
            questions = asset.question_set.question.filter(category_id=category_id["category"])
            data[category.title] = questions
        return data
    
    def handle_invalid_form(self, context, form, request, survey):
        return render(request, self.template_name, context)

    def treat_valid_form(self, form, kwargs, request, asset, preventivemaintenance):
        save_form = PreventiveMaintenanceQuestionAnswerForm(
            request.POST,
            request.FILES or None,
            slug=kwargs["slug"],
            asset=asset,
            user=request.user
            )
        if save_form.is_valid():
            save_form.save(preventivemaintenance=preventivemaintenance)
        else:
            context = {
                "forms": form,
                "asset": asset,
                "categories": form.current_categories
            }
            return self.handle_invalid_form(context, form, request, asset)
        
        preventivemaintenance_id = preventivemaintenance.id
        if request.GET:
            urlbind_with_get_request = (
                reverse(
                    "preventivemaintenance:preventive_maintenance_detail",
                    kwargs={"pk": preventivemaintenance_id}
                )
                + "?" + request.GET.urlencode()
            )
        else: 
            urlbind_with_get_request = reverse(
                "preventivemaintenance:preventive_maintenance_detail",
                kwargs={"pk":preventivemaintenance_id}
            )

        return redirect(urlbind_with_get_request)