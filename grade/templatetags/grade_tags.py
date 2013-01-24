# coding: utf-8

# django
from django.template import Library

# models
from grade.models import Talk

# Habilitando o registro de novos filtros e tags
register = Library()


@register.inclusion_tag('tags/display_talks.html')
def display_talks(day, hour, minute):
    """ Show fisl talks given a day and hour """

    return {'talks': Talk.objects.filter(date=day, hour=hour, minute=minute)}

@register.inclusion_tag('tags/display_talks.html')
def display_talks_zone(day, hour, minute, zone):
    """ Show fisl talks given a day, hour and zone """

    return {'talks': Talk.objects.filter(date=day, hour=hour, minute=minute, zone=zone)}

@register.inclusion_tag('tags/display_talks.html')
def display_talks_room(day, hour, minute, room):
    """ Show fisl talks given a day, hour and room """

    return {'talks': Talk.objects.filter(date=day, hour=hour, minute=minute, room=room)}

@register.inclusion_tag('tags/display_talks.html')
def display_talks_next_hour(day, next_hour):
    """ Show fisl talks at the next hour """

    return {'talks': Talk.objects.filter(date=day, hour=next_hour)}
