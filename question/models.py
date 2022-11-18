from xml.dom import ValidationErr
from django.db import models
from systemandfacility.models import Facility
from common.models import BaseModel
from django.conf import settings
from django.core.exceptions import ValidationError
 

TEXT = "text"
SHORT_TEXT = "short-text"
RADIO = "radio"
SELECT = "select"
SELECT_IMAGE = "select_image"
SELECT_MULTIPLE = "select-multiple"
INTEGER = "integer"
FLOAT = "float"
DATE = "date"

QUESTION_TYPES = (
    (TEXT,("text (multiple line)")),
    (SHORT_TEXT,("short text (one line)")),
    (RADIO,("radio")),
    (SELECT,("select")),
    (SELECT_MULTIPLE,("Select Multiple")),
    (SELECT_IMAGE,("Select Image")),
    (INTEGER,("integer")),
    (FLOAT,("float")),
    (DATE,("date")),
)

class QuestionCategory(BaseModel):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="categories")
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    order = models.IntegerField(blank=True, null=True)
    is_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(BaseModel):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="questions")
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    answer_type = models.CharField(choices=QUESTION_TYPES, max_length=50)
    choices = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="parent_question", blank=True, null=True)
    parent_answer = models.TextField(blank=True, null=True)
    correct_answer = models.TextField(blank=True, null=True)
    question_text = models.TextField()

    def __str__(self):
        if self.parent:
            text = self.question + "(" + self.parent.question + ")"
        else:
            text = self.question
        return text

    def save(self, *args, **kwargs):
        if self.answer_type in [RADIO, SELECT, SELECT_MULTIPLE]:
            self.validate_choices(self.choices)
        super(Question, self).save(*args, **kwargs)

    def validate_choices(self, choices):
        values = choices.split(settings.CHOICES_SEPARATOR)
        empty = 0

        for value in values:
            if value.replace(" ", "") == "":
                empty += 1

        if len(values) < 2 + empty:
            message = "Selected field requires an associated list of choices."
            raise ValidationError(message)
    
    def get_all_child_questions(self, include_self=True, category_is_comment=True):
        child_questions = []
        if include_self:
            child_questions.append(self)
        
        for child_question in Question.objects.filter(parent=self).exclude(
            category__is_comment=category_is_comment
        ):
            _child_questions = child_question.get_all_child_questions(include_self=True)

            if len(_child_questions) > 0:
                child_questions.extend(_child_questions)

        return child_questions

    def get_all_child_questions_by_category(self, include_self=True):
        child_questions = []
        if include_self:
            child_questions.append(self)

        for child_question in Question.objects.filter(parent=self, category=self.category):
            _child_questions = child_question.get_all_child_questio_by_category(include_self=True)

            if len(_child_questions) > 0:
                child_questions.extend(_child_questions)

        return child_questions    


class QuestionSet(BaseModel):
    name = models.CharField(max_length=50)
    question = models.ManyToManyField(Question, related_name="questionsets")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

