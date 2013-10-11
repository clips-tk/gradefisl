# coding: utf-8

# django
from django.template import Library

# models
from clips.models import Talk

# Habilitando o registro de novos filtros e tags
register = Library()


@register.inclusion_tag('tags/display_talks.html')
def display_talks(day, hour):
    """ Show talks given a day and hour """

    return {'talks': Talk.objects.filter(date__contains=day.date) \
    .filter(date__contains=hour), 'hour': hour}


@register.inclusion_tag('tags/display_talks.html')
def display_talks_zone(day, hour, zone):
    """ Show fisl talks given a day, hour and zone """

    return {'talks': Talk.objects.filter(zone=zone, date__contains=day.date) \
    .filter(date__contains=hour), 'hour': hour}


@register.inclusion_tag('tags/display_talks.html')
def display_talks_room(day, hour, room):
    """ Show talks given a day, hour and room """

    return {'talks': Talk.objects.filter(room=room, date__contains=day.date) \
    .filter(date__contains=hour), 'hour': hour}


@register.inclusion_tag('tags/display_talks.html')
def display_talks_now(now, last_session):
    """ Show talks ocurring now"""

    return {'talks': Talk.objects.filter(date__lte=now) \
    .filter(date__gte=last_session)}


@register.inclusion_tag('tags/display_talks.html')
def display_talks_next_session(now, next_session):
    """ Show talks at the next session """

    return {'talks': Talk.objects.filter(date__gte=now) \
    .filter(date__lte=next_session)}
