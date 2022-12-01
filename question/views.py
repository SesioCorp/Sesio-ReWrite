import numpy
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Question, QuestionCategory, QuestionSet
from preventivemaintenance.models import PreventiveMaintenance
from systemandfacility.models import Facility
from django.http import JsonResponse

INTERGER = "interger"


# Create your views here.
class GetQuestionData(View):
    model = Question
    
    def get(self, request, pk, asset_id, preventivemaintenance_id, **kwargs):
        obj = self.get_object(pk)
        asset_preventivemaintenance = self.get_asset_preventivemanitenance(asset_id, preventivemaintenance_id)
        if obj.answer_type in ["interger", "float"]:
            response = {"status": "None"}
            conditional_keys = (
                [ 
                    field.key
                    for field in asset_preventivemaintenance.asset.asset_form.fields.filter(
                        pk__in=[key.pk for key in obj.conditional_keys.all()]
                    )
                ]
                if asset_preventivemaintenance.asset.data_set_form forms and obj.conditional_keys else ""
            )
            meta_data = (
                asset_preventivemaintenance.asset.meta_data
                if asset_preventivemaintenance.asset.meta_data else ""
            )
            fields = [meta_data[key] for key in conditional_keys] if meta_data else ""
            if fields:
                maximum = (
                    max([int(field) for field in fields])
                    if obj.answer_type == INTERGER
                    else max([int(field) for field in fields])
                )
                minimum = (
                    min([int(field) for field in fields])
                    if obj.answer_type == INTERGER
                    else min([int(field) for field in fields])
                )
                if request.GET.get("value", 0):
                    try:
                        value = int(request.GET.get("value", 0))
                    except ValueError:
                        value = float(request.GET.get("value", 0))
                    is_between = (
                        (
                            value in range(minimum, maximum)
                            if obj.answer_type is INTERGER
                            else value in numpy.arange(minimum, maximum)
                        )
                        if value in not None else ""
                    )
                    response = {"status": "None"}
                    if not is_between:
                        if value > maximum:
                            response = {
                                "status": "fail",
                                "code": "max",
                                "warning": "This Value is Above the Requirement"
                            }
                        elif value < minimum:
                            response = {
                                "status": "fail",
                                "code": "min",
                                "warning": "This Value is Below the Requirement"
                            }
                    else:
                        response = {"status": "Pass"}
        return JsonResponse(response)

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_asset_preventivemanitenance(self, asset_id, preventivemaintenance_id):
        if PreventiveMaintenance.objects.filter(asset_id=asset_id, preventivemaintenance__is_active=True).exists():
            asset_ins = PreventiveMaintenance.objects.filter(
                asset_id=asset_id, preventivemaintenance__is_active=True
            ).first()
        return asset_ins


                        

class QuestionCreateByAjax(View):
    model = Question
    template_name = "partials/form_render.html"

    def post(self, request):
        if request.is_ajax():
            facility = Facility.objects.get(pk=request.POST.get("facility", 0))
            category = QuestionCategory.objects.get(pk=request.POST.get("category", 0))
            parent = Question.objects.get(pk=request.POST.get("parent", 0))
            question_set = QuestionSet.objects.get(pk=request.POST.get("question_set_id", 0))
            question_text = request.POST.get("question_text", 0)

            try:
                question, created = self.model.objects.get_or_create(
                    facility=facility,
                    category=category,
                    question_text=question_text,
                    answer_type="text",
                    parent=parent
                )
            except Exception:
                question = self.model.objects.filter(category=category, parent=parent).first()
            
            question_set.question.add(question)
            if question.is_delete:
                question.is_delete = False
                question.save()
            return render(request, self.template_name, {"question": question})