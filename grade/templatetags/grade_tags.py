# coding: utf-8

# django
from django.template import Library

# models
from grade.models import Talk

# Habilitando o registro de novos filtros e tags
register = Library()


@register.inclusion_tag('tags/display_talks.html')
def display_talks(day, hour):
    """ Show fisl talks given a day and hour """

    return {'talks': Talk.objects.filter(date=day, hour=hour)}
