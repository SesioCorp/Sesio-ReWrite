from django.db import models
from question.models import Question
from django.conf import settings
from preventivemaintenance.models import PreventiveMaintenance
from common.models import BaseModel

class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer", blank=True, null=True)
    answer_type_text_number = models.TextField(blank=True, null=True)
    answer_type_text = models.TextField(blank=True, null=True)
    answer_type_integer = models.IntegerField(blank=True, null=True)
    answer_type_float = models.FloatField(blank=True, null=True)
    answer_type_boolean = models.BooleanField(blank=True, null=True)
    answer_type_image = models.ImageField(upload_to="answer/", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answer", blank=True, null=True)
    preventive_maintenance = models.ForeignKey(PreventiveMaintenance, on_delete=models.CASCADE, related_name="answer", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_fail = models.BooleanField(default=False)

    def __str__(self):
        if self.answer_type_text:
            return self.answer_type_text

        elif self.answer_type_integer:
            return self.answer_type_integer

        elif self.answer_type_float:
            return self.answer_type_float

        elif self.answer_type_boolean:
            if self.answer_type_boolean == True:
                return "Yes"

            else: return "No"

        elif self.answer_type_image:
            return "Image Type Answer"
    
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"