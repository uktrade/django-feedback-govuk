from django import template
from django.conf import settings

from django_feedback_govuk.forms import FeedbackForm

register = template.Library()


@register.inclusion_tag("django_feedback_govuk/partials/submit.html", takes_context=True)
def feedback_submit(context):
    if 'form' in context:
        form = context['form']
    else:
        initial = {}
        initial["submitter"] = context.request.user
        form = FeedbackForm(initial=initial)

    return {
        "form": form,
        "service_name": settings.DJANGO_FEEDBACK_GOVUK["SERVICE_NAME"],
    }


@register.inclusion_tag("django_feedback_govuk/partials/confirm.html")
def feedback_confirm():
    return {}


@register.inclusion_tag("django_feedback_govuk/partials/listing.html", takes_context=True)
def feedback_listing(context):
    return context


@register.filter()
def get_elided_page_range(page):
    return page.paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)


@register.simple_tag(takes_context=True)
def get_pagination_url(context, page):
    request = context["request"]

    query_params = request.GET.copy()
    query_params["page"] = page

    return "?" + query_params.urlencode()
