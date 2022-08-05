from tkinter import CASCADE
from django.db import models
from systemandfacility.models import Facility
 

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

class QuestionCategory(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="categories")
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    order = models.IntegerField(blank=True, null=True)
    is_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="questions")
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    answer_type = models.CharField(choices=QUESTION_TYPES, max_length=50)
    choices = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="childs")
    parent_answer = models.TextField(blank=True, null=True)
    correct_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.parent:
            text = self.question + "(" + self.parent.question + ")"
        else:
            text = self.question
        return text

class QuestionSet(models.Model):
    name = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="questionsets")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

