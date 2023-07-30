from django.conf import settings
from django.core.paginator import Paginator


def get_page(queryset, request, number_of_posts=settings.COUNT_POST):
    return Paginator(queryset, number_of_posts).get_page(
        request.GET.get("page")
    )
