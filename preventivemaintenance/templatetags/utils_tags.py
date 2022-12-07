from urllib import request
from django import template
from django.conf import settings
from django.core.paginator import Paginator
from preventivemaintenance.questionanswerform import PreventiveMaintenanceQuestionAnswerForm

register = template.Library()

def get_current_page_size(request, default=None):
    page_size = default or settings.PAGINATION_DEFAULT_PAGINATION
    
    try:
        page_size = int(request.GET.get("page_size"))
    except (ValueError, TypeError):
        pass

    if page_size <= 0:
        page_size = default or settings.PAGINATION_DEFAULT_PAGINATION
    return min(page_size, settings.PAGINATION_MAX_SIZE)

@register.simple_tag(takes_context=True)
def qs_paginator(context, qs):
    request = context.request
    paginator = Paginator(qs, get_current_page_size(request))
    page_number = request.GET.get(settings.PAGINATION_PAGE_PARAM)
    page = paginator.get_page(page_number)
    return page

@register.simple_tag()
def get_preventivemaintenance_form(slug, asset, user, step):
    form = PreventiveMaintenanceQuestionAnswerForm(slug=slug, asset=asset, user=user, step=step)
    return form


@register.simple_tag()
def get_question_choices(choices_str):
    return [choice.strip() for choice in choices_str.split(",")]


@register.simple_tag()
def get_answer(question, preventivemaintenance):
    if Answer.objects.filter(question=question, preventive_maintenance=preventivemaintenance, is_active=True).exists():
        answer = Answer.objects.get(question=question, preventive_maintenance=preventivemaintenance)
        answer_dict = {
            "parent_answer": "",
            "image": ""
        }
        if question.answer_type == "select":
            try:
                child_answer = Answer.objects.get(question=question.parent_question.first(), preventive_maintenance=preventivemaintenance, is_active=True)
                if answer and child_answer is not None and answer_type_text_number.lower() in child_answer.question.parent_answer.split(","):
                    image_url = child_answer.answer_type_image.url
                else:
                    image_url = None
            except Exception:
                image_url = None
            
            answer_dict["parent_answer"] = answer.answer_type_text_number
            answer_dict["image"] = image_url
            return answer_dict

        if question.answer_type == "radio":
            try:
                child_answer = Answer.objects.get(question=question.parent_question.first(), preventive_maintenance=preventivemaintenance, is_active=True)
                if answer and child_answer is not None and answer_type_text_number.lower() in child_answer.question.parent_answer.split(","):
                    image_url = child_answer.answer_type_image.url
                else:
                    image_url = None
            except Exception:
                image_url = None
            
            answer_dict["parent_answer"] = answer.answer_type_text_number
            answer_dict["image"] = image_url
            return answer_dict
        
        
