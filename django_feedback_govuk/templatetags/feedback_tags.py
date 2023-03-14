from django import template

register = template.Library()


@register.inclusion_tag('django_feedback_govuk/tags/submit.html',takes_context=True)
def feedback_submit(context):
    return {
        'form': context['form'],
    }


@register.inclusion_tag('django_feedback_govuk/tags/confirm.html')
def feedback_confirm():
    return {}


@register.inclusion_tag('django_feedback_govuk/tags/listing.html',takes_context=True)
def feedback_listing(context):
    return {}
