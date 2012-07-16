# coding: utf-8

from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, TemplateView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

# fisl
from grade.models import Room, Area, Zone, Author, Talk


class IndexView(TemplateView):
    """ View da homepage """

    template_name = "grade/index.html"


class SearchView(TemplateView):
    """ View do buscador de palestras """

    template_name = "grade/search.html"


class TalkDetailView(DetailView):
    """ View utilizada para mostrar a palestra """

    model = Talk
    context_object_name = 'talk'


class TalkListView(TemplateView):
    """ View utilizada para mostrar as palestras """

    template_name = "grade/talks_list.html"

    def get_context_data(self, **kwargs):
        context = super(TalkListView, self).get_context_data(**kwargs)

        days = Talk.objects.dates("date", "day")
        hours = map(lambda x: str(x).zfill(2), range(9, 19))

        context['user'] = self.request.user
        context['days'] = days
        context['hours'] = hours

        return context

class ZoneDetailView(DetailView):
    """ View utilizada para mostrar as palestras por zona """

    model = Zone
    template_name = "grade/zone_talk_list.html"

    def get_context_data(self, **kwargs):
        context = super(ZoneDetailView, self).get_context_data(**kwargs)

        days = self.get_object().talk_set.all().dates("date", "day")
        hours = map(lambda x: str(x).zfill(2), range(9, 19))

        context['zone'] = self.get_object()
        context['user'] = self.request.user
        context['days'] = days
        context['hours'] = hours

        return context

class RoomDetailView(DetailView):
    """ View utilizada para mostrar as palestras por sala """

    model = Room
    template_name = "grade/room_talk_list.html"

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)

        days = self.get_object().talk_set.all().dates("date", "day")
        hours = map(lambda x: str(x).zfill(2), range(9, 19))

        context['zone'] = self.get_object()
        context['user'] = self.request.user
        context['days'] = days
        context['hours'] = hours

        return context

class AuthorDetailView(DetailView):
    """ View utilizada para mostrar o autor e sua lista de palestras """

    model = Author
    context_object_name = 'author'


def clean_data():
    """ Clean the grade models """

    grade_models = [Room, Area, Talk, Zone, Author]
    clear_data = lambda x: x.objects.all().delete()

    for grade_model in grade_models:
        clear_data(grade_model)


@login_required
def choice_talk(request, talk_id):
    talk = Talk.objects.get(id=talk_id)

    if not talk.listeners.filter(id=request.user.id).count():
        talk.listeners.add(request.user)
        talk.save()

    return HttpResponseRedirect(reverse('grade:talk', args=[talk_id]))


def gerar_rooms(json):
    for room in json['rooms']:
        if not Room.objects.filter(uid=room['room_id']).count():
            Room.objects.create(uid=room['room_id'],
                                capacity=room['capacity'],
                                name=room['name'],
                                translation=room['translation'],
                                position=room['position'])


def gerar_areas(json):
    for area in json['areas']:
        if not Area.objects.filter(uid=area['area_id']).count():
            Area.objects.create(uid=area['area_id'], name=area['name'])


def gerar_zones(json):
    for zone in json['zones']:
        if not Zone.objects.filter(uid=zone['zone_id']).count():
            Zone.objects.create(uid=zone['zone_id'], name=zone['name'])


def gerar_authors(json):
    for author in json['authors']:
        if not Author.objects.filter(uid=author['author_id']).count():
            Author.objects.create(uid=author['author_id'],
                                  candidate=author['candidate'],
                                  name=author['name'])


def gerar_talks(json):
    gerar_areas(json)
    gerar_rooms(json)
    gerar_zones(json)
    gerar_authors(json)

    for talk in json['talks']:
        if not Talk.objects.filter(area=talk['area_id']).count():
            t = Talk(area=Area.objects.get(uid=talk['area_id']),
                     room=Room.objects.get(uid=talk['room_id']),
                     zone=Zone.objects.get(uid=talk['zone_id']),
                     level=talk['level'],
                     hour=talk['hour'],
                     minute=talk['minute'],
                     date=talk['date'],
                     abstract=talk['abstract'],
                     title=talk['title'])

            # To get the id
            t.save()

            # Now we tie the authors to the talk
            t.authors = Author.objects.filter(candidate=talk['candidate'])
            t.save()


def gerar_grade(request):
    data_json = open("public/json/data.json", "r").read()
    json = simplejson.loads(data_json)

    gerar_talks(json)

    return HttpResponse("Grade gerada com sucesso!")
