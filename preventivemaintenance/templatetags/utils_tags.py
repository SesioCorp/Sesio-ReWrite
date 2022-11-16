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


