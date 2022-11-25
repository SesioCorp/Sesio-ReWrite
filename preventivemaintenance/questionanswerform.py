from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from answer.models import Answer
from preventivemaintenance.models import PreventiveMaintenance
from question.models import SHORT_TEXT, Question, QuestionCategory, QuestionSet
from users.models import CustomUser
from django.utils.text import slugify


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
        self.steps_count = len(self.categories)
        self.question_step_count = 0
        self.answers = False
        self.add_questions()
        self.__add_extra_fields()

    def add_questions(self):

        if self.step is not None:
            questions = []
            for question in self.qs_step():
                questions.append(question)
                answer = self._get_preexisting_answer(question)

                if answer is not None:
                    child_questions = question.get_all_child_question_by_category(include_self=False)
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
                    
                for question in questions:
                    if question.category.is_comment is True and question.parent:
                        answer = Answer.objects.filter(
                            question=question,
                            preventive_maintenance = self.preventivemaintenance
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


    def qs_step(self):
        if self.step == len(self.categories):
            qs_step = (
                self.asset.question_set.question.filter(
                    category__isnull=True, category_id=self.categories[self.step]
                    ).prefetch_related("question").order_by("order", "id")
            )
        elif self.categories[self.step].is_comment:
            qs_step = self.asset.question_set.question.filter(
                category_id = self.categories[self.step],
                deleted = False
            ).order_by("order", "id")

        else:
            qs_step = self.asset.question_set.question.filter(
                category_id = self.categories[self.step],
                parent__isnull = True
            ).order_by("order", "id")

        return qs_step
        

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
        
        field.widget.attrs["comment_category_id"] = (
            self.asset.question_set.question.filter(category__is_comment=True).first().category.pk
            if self.asset.question_set.question.filter(category__is_comment=True).exists() else ""
        )

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

        field.widget.attrs["parent_id"] = (
            "id_parent_" + str(question.parent.id) if question.parent else ""
        )

        field.widget.attrs["question_text"] = question.question_text

        field.widget.attrs["question_child_count"] = (
            len(question.parent.get_all_child_questions(include_self=False))
        )

        field.widget.attrs["question_parent_child_count"] = (
            len(question.parent.get_all_child_questions(include_self=False)) 
            if question.parent else ""
        )

        field.widget.attrs["child_questions"] = ",".join(
            [
                str(obj.pk) for obj in question.get_all_child_questions(include_self=False)
            ]
        )

        field.widget.attrs["parent_question_ids"] = ",".join(
            [
                str(obj.parent.pk) for obj in question.get_all_child_questions(include_self=False)
            ]
        )
        field.widget.attrs["parent_question_text"] = (
            question.parent.question_text
            if question.parent and 
            len(question.parent.get_all_child_questions(include_self=False)) ==2
            else ""
        )
        field.widget.attrs["question_set_id"] = self.asset.question_set.pk

        if question.answer_type == RADIO:
            field.widget.attrs["required"] = True
        
        if question.answer_type == SELECT_IMAGE:
            field.widget.attrs["class"] = "form-control"

        if question.answer_type == DATE:
            field.widget.attrs["class"] = "date"

        self.fields["question_%d" % question.pk] = field


    def __add_extra_fields(self):

        existing_fields_keys = self.fields.keys()
        form_data = self.data.copy()

        if len(form_data) - 1 > len(existing_fields_keys):
            form_data.pop("csrfmiddlewaretoken", None)
            form_data.pop("save_and_exit", None)
            
            if self.files:
                files_data = self.files.copy()
                self.append_question_by_extra_field_keys(files_data.keys(), existing_fields_keys)
            
            self.append_question_by_extra_field_keys(form_data.keys(), existing_fields_keys)
        
        elif len(form_data) < len(existing_fields_keys) and len(form_data) != 0:
            delete_fields = []
            
            for field_key in existing_fields_keys:
                if field_key not in form_data.keys():
                    delete_fields.append(field_key)
            
            for field in delete_fields:
                self.fields.pop(field)
            

    def append_question_by_extra_field_keys(self, field_dict_keys, existing_field_keys):

        for field_name in field_dict_keys:
            if field_name not in existing_field_keys:
                question_id = field_name.split("_")[1]
                question = Question.objects.get(pk=question_id)
                self.add_question(question)


    
    
    def get_question_widget(self, question):
        try:
            return self.WIDGETS[question.answer_type]

        except KeyError:
            return None

    
    @staticmethod
    def get_question_choices(question):
        question_choices = None

        if question.answer_type not in [TEXT, SHORT_TEXT, INTEGER, FLOAT, DATE]:
            question_choices = question.get_choices()

            if question.answer_type in [SELECT]:
                question_choices = tuple([("", "----")]) + question_choices
        
        return question_choices

    def get_question_field(self, question, **kwargs):
        try:
            return self.FIELDS[question.answer_type](**kwargs)
        except KeyError:
            return forms.ChoiceField(**kwargs)

    
    def current_categories(self):

        if self.step is not None and self.step < len(self.categories):
            return [self.categories[self.step]]

        return [QuestionCategory(title="NO category", description="NO cat desc")]

    
    def has_next_step(self):
        
        if self.step < self.steps_count - 1:
            return True
        
        return False

    def next_step_url(self):

        if self.has_next_step():
            context = {
                "slug": self.slug,
                "pk": self.asset.id,
                "step": self.step + 1
            }

            return reverse("preventivemaintenance:preventive-maintenance-question-answer-form-step", kwargs=context)
        
    
    def _get_preexisting_answers(self):
        
        if self.answers:
            return self.answers

        try:
            answers = Answer.objects.filter(preventive_maintenance=self.preventivemaintenance).prefetch_related("question")
            self.answers = {
                answer.question.id: answer for answer in answers.all()
            }

        except Answer.DoesNotExist:
            self.answers = None
        
        return self.answers
    

    def _get_preexisting_answer(self, question):
        answers = self._get_preexisting_answers()
        return answers.get(question.id, None)


    def get_question_initial(self, question, data):
        initial = None
        answer = self._get_preexisting_answer(question)

        if answer:
            if question.answer_type == SELECT_MULTIPLE:
                initial = []

                if answer.answer_type_text_number == "[]":
                    pass
                
                elif ("[" in answer.answer_type_text_number and "]" in answer.answer_type_text_number):
                    initial = []
                    unformatted_choices = answer.answer_type_text_number[1:-1].strip()

                    for unformatted_choice in unformatted_choices.split(settings.CHOICES_SEPARATOR):
                        choice = unformatted_choice.split("'")[1]
                        initial.append(slugify(choice))

                else:
                    initial.append(slugify(answer.answer_type_text_number))
            
            elif question.answer_type == SELECT_IMAGE:
                initial = answer.answer_type_image

            elif question.answer_type == INTEGER:
                initial = answer.answer_type_integer

            elif question.answer_type == FLOAT:
                initial = answer.answer_type_float

            else:
                initial = answer.answer_type_text_number

        if data:
            initial = data.get("question_%d" % question.pk)

        return initial

    
    def get_answer_by_preventive_maintenance(question, preventivemaintenance):

        if Answer.objects.filter(
            question=question,
            preventive_maintenance=preventivemaintenance,
            is_active=True
        ).exists():
            answer = Answer.objects.filter(
                question=question,
                preventive_maintenance=preventivemaintenance
            ).last()
            answer_dict = {
                "parent_answer": "",
                "image": ""
            }

            if question.answer_type in ["select", "radio"]:
                parent_question_answer = (
                    question.parent_question.filter(category=question.category).first().parent_answer
                    if question.parent_question.filter(category=question.category).exists() else ""
                )

                if answer.answer_type_text_number in parent_question_answer:
                    try:
                        child_answer = Answer.objects.get(
                            question=question.parent_question.filter(category=question.category).first(),
                            preventive_maintenance=preventivemaintenance,
                            is_active=True
                        )
                        image_url = child_answer.answer_type_image.url
                    
                    except Exception:
                        image_url = None
                
                else:
                    image_url = None
                
                answer_dict["answer"] = answer.answer_type_text_number

                return answer_dict

            elif question.answer_type in ["select_image"]:
                parent_question_answer = (
                    question.parent_question.filter(category=question.category).first().parent_answer
                    
                    if question.parent_question.filter(category=question.category).exists() else ""
                )

                if answer.answer_type_text_number == parent_question_answer:
                    try:
                        child_answer = Answer.objects.get(
                            question = question,
                            preventive_maintenance=preventivemaintenance,
                            is_active=True
                        )
                        image_url = child_answer.answer_type_image.url

                    except Exception:
                        image_url = None
            
                else:
                    image_url = None
                
                answer_dict["parent_answer"] = "pass" if image_url is None else "fail"
                answer_dict["image"] = image_url

                return answer_dict

            answer_dict["parent_answer"] = "pass"
            
            return answer_dict

        else:
            return None

        
    def save(self, commit=True, *args, **kwargs):

        response = super(PreventiveMaintenanceQuestionAnswerForm, self).save(commit=False)
        preventivemaintenance = kwargs.pop("preventivemaintenance", None)

        for field_name, field_value in list(self.cleaned_data.items()):
            
            if field_name.startswith("question_"):
                question_id = int(field_name.split("_")[1])

                try:
                    question = Question.objects.get(pk=question_id)
                    answer = self._get_preexisting_answer(question)

                except Exception:
                    answer = None

                if answer is None:
                    answer = Answer(questions=question)
                
                if question.answer_type in [TEXT, SHORT_TEXT, SELECT, RADIO, DATE]:
                    answer.answer_type_text_number = field_value
                elif question.answer_type in [FLOAT]:
                    answer.answer_type_float = field_value
                elif question.answer_type in [INTEGER]:
                    answer.answer_type_integer = field_value
                elif question.answer_type in [SELECT_IMAGE]:
                    answer.answer_type_image = field_value
                
                answer.user = CustomUser.objects.all().last()
                answer.preventive_maintenance = preventivemaintenance
                answer.is_active = True
                status = get_answer_by_preventive_maintenance(question, preventivemaintenance)["parent_answer"]

                if status.lower() == "fail":
                    answer.is_fail = True
                    answer.repair_due_date = (
                        answer.preventive_maintenance.updated_at + timezone.timedelta(days = 45))
                    answer.save()
                else:
                    answer.is_fail = False
                    answer.save()
        return response