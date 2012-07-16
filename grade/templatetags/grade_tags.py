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

@register.inclusion_tag('tags/display_talks_zone.html')
def display_talks_zone(day, hour, zone):
    """ Show fisl talks given a day, hour and zone """

    return {'talks': Talk.objects.filter(date=day, hour=hour, zone=zone)}

@register.inclusion_tag('tags/display_talks.html')
def display_talks_room(day, hour, room):
    """ Show fisl talks given a day, hour and room """

    return {'talks': Talk.objects.filter(date=day, hour=hour, room=room)}
