from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Question, QuestionCategory, QuestionSet
from preventivemaintenance.models import preventivemaintenance
from systemandfacility.models import Facility


# Create your views here.
class GetQuestionData(View):
    pass


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