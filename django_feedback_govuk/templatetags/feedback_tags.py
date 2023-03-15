from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('django_feedback_govuk/tags/submit.html', takes_context=True)
def feedback_submit(context):
    return {
        'form': context['form'],
        'service_name': settings.DJANGO_FEEDBACK_GOVUK['SERVICE_NAME']
    }


@register.inclusion_tag('django_feedback_govuk/tags/confirm.html')
def feedback_confirm():
    return {}


@register.inclusion_tag('django_feedback_govuk/tags/listing.html',takes_context=True)
def feedback_listing(context):
    return {
        'paginator': context['paginator'],
        'page_obj': context['page_obj'],
        'is_paginated': context['is_paginated'],
        'object_list': context['object_list'],
        'feedback_list': context['feedback_list'],
    }
