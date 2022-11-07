from genericpath import exists
from socket import fromshare
from tkinter.tix import Form
from unicodedata import category
from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from answer.models import Answer
from preventivemaintenance.models import PreventiveMaintenance
from question.models import SHORT_TEXT, Question, QuestionCategory
from users.models import CustomUser


TEXT = "text"
SHORT_TEXT = "short_text"
RADIO = "radio"
SELECT = "select"
SELECT_IMAGE = "select_image"
SELECT_MULTIPLE = "select_multiple"
INTEGER = "integer"
FLOAT = "float"
DATE = "date"


class PreventiveMaintenanceQuestionAnswerForm(forms.models.ModelForm):
    FIELDS = {
        TEXT: forms.CharField,
        SHORT_TEXT: forms.CharField,
        SELECT_MULTIPLE: forms.MultipleChoiceField,
        INTEGER: forms.IntegerField,
        FLOAT: forms.FloatField,
        DATE: forms.DateField,
        SELECT_IMAGE: forms.ImageField,
        RADIO: forms.RadioSelect,
        SELECT: forms.Select
    }

    WIDGETS = {
        TEXT: forms.Textarea,
        SHORT_TEXT: forms.TextInput,
        SELECT_MULTIPLE: forms.CheckboxSelectMultiple,
        RADIO: forms.RadioSelect,
        SELECT: forms.Select
    }

    class Meta:
        model = Answer
        fields = ()

    def __init__(self, *args, **kwargs):

        #Initialize the Form
        
        self.questions = []

        self.asset = kwargs.pop("asset")
        self.slug = kwargs.pop("slug")

        if self.slug:
            try:
                self.preventivemaintenance = PreventiveMaintenance.objects.get(slug=self.slug)
            
            except Exception as error:
                raise error
        
        self.user = kwargs.pop("user")

        try:
            self.step = int(kwargs.pop("step"))

        except KeyError:
            self.step = None
        
        try:
            self.question_step = int(kwargs.pop("question_step"))
        
        except KeyError:
            self.question_step = None

        super(PreventiveMaintenanceQuestionAnswerForm, self).__init__(*args, **kwargs)
        self.categories = self.asset.get_question_categories()
        self.question_step_count = 0
        self.answer = False
        self.add_questions()
        self.__add_extra_fields()


    def question_step(self):
        if self.step == len(self.categories):
            question_step = (
                self.asset.question_set.question.filter(
                    category__isnull=True, category_id=self.categories[self.step]
                    ).prefetch_related("question").order_by("order", "id")
            )
        elif self.categories[self.step].is_comments:
            question_step = self.asset.question_set.filter(
                category_id = self.categories[self.step],
                deleted = False
            ).order_by("order", "id")

        else:
            question_step = self.asset.question_set.filter(
                category_id = self.categories[self.step],
                parent__isnull = True
            ).order_by("order", "id")

        return question_step

    def get_child_questions(self):
        child_questions = self.questions.get_all_child_question_by_category(include_self=False)
        index = 0

        for child_question in child_questions:
            answer = (
                answer if index == 0 else self._get_preexisting_answer(child_question.parent)
            )

            if child_question is not None and answer.is_fail:
                self.questions.append(child_question)

            else:
                break

            index += 1

    def get_comment_questions(self):
        for question in self.questions:
            if question.category.is_comments is True and question.parent:
                answer = Answer.objects.filter(
                    question=question,
                    preventivemaintenance = self.preventivemaintenance
                )
                parent_answer = self._get_preexisting_answer(question.parent)
                parent_child_question = (
                    question.parent.parent_question.filter(category=question.parent.category).first()
                    if question.parent.parent_question.filter(category=question.parent.category).exists()
                    else None
                )

                if (
                    answer.exists() and parent_answer and parent_child_question is not None
                ):
                    self.add_question(question)

            else:
                self.add_question(question)

    def add_question(self, question, data=0):
        kwargs = {"label": question.question_text, "required": False}
        initial = self.get_question_initial(question, data)

        if initial:
            kwargs["initial"] = initial

        choices = (self.get_question_choices(question) if question.answer_type in [SELECT, RADIO, SELECT_MULTIPLE] else "")

        if choices:
            kwargs["choices"] = choices
        
        widget = self.get_question_widget(question)

        if widget:
            kwargs["widget"] = widget

        field = self.get_question_field(question, **kwargs)

        field.widget.attrs["category_id"] = (question.category.pk if question.category else "")
        
        field.widget.attrs["comment_category_id"] = (self.asset.question_set.question.filter(category__is_comments=True).first().category.pk
        if self.asset.question_set.question.filter(category__is_comments=True).exists() else "")

        field.widget.attrs["fail_condition_answer"] = (
            question.parent_question.filter(category=question.category).first().parent_answer
            if question.parent_question.filter(category=question.category).exists() else ""
        )
        
        field.widget.attrs["preventivemaintenance_slug"] = (
            self.preventivemaintenance.slug if self.preventivemaintenance.slug else ""
        )

        field.widget.attrs["preventivemaintenance_id"] = (
            self.preventivemaintenance.pk if self.preventivemaintenance else ""
        )

        field.widget.attrs["facility_id"] = (
            self.preventivemaintenance.facility.pk if self.preventivemaintenance.facility else ""
        )

        field.widget.attrs["asset_name"] = (self.asset.slug if self.asset else "")

        field.widget.attrs["asset_id"] = (
            self.asset.pk if self.asset else ""
        )



    def add_questions(self):

        if self.step is not None:
            for question in self.question_step():
                self.questions.append(question)
                answer = self._get_preexisting_answer(question)

                if answer is not None:
                    self.get_child_questions()
                    self.get_comment_questions()

    
        
                        
