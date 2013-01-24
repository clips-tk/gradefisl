# coding: utf-8

from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, TemplateView, ListView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.db.models import Q

# fisl
from grade.models import Room, Area, Zone, Author, Talk


class IndexView(TemplateView):
    """ View da homepage """

    template_name = "grade/index.html"


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
        hours = map(lambda x: str(x).zfill(2), range(10, 20))

        context['user'] = self.request.user
        context['days'] = days
        context['hours'] = hours

        return context


class ZoneDetailView(DetailView):
    """ View utilizada para mostrar as palestras por trilha """

    model = Zone
    template_name = "grade/zone_talk_list.html"

    def get_context_data(self, **kwargs):
        context = super(ZoneDetailView, self).get_context_data(**kwargs)

        days = self.get_object().talk_set.all().dates("date", "day")
        hours = self.get_object().talk_set.all().values_list('hour','minute').distinct().order_by('hour','minute')

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
        hours = self.get_object().talk_set.all().values_list('hour','minute').distinct().order_by('hour','minute')

        context['zone'] = self.get_object()
        context['user'] = self.request.user
        context['days'] = days
        context['hours'] = hours

        return context


class NowListView(TemplateView):
    """ View utilizada para mostrar as próximas palestras da grade """

    template_name = "grade/now_talk_list.html"

    def get_context_data(self, **kwargs):
        context = super(NowListView, self).get_context_data(**kwargs)

        context['user'] = self.request.user
        context['day'] = date.today()
        context['hour'] = datetime.now().hour
        context['next_hour'] = datetime.now().hour + 1

        return context


class DayTalkListView(ListView):
    """ View utilizada para mostrar as palestras por dia"""

    template_name = "grade/talks_list.html"

    def get_queryset(self):
        self.date_url = Talk.objects.dates("date", "day")[int(self.args[0])]

    def get_context_data(self, **kwargs):
        context = super(DayTalkListView, self).get_context_data(**kwargs)

        hours = Talk.objects.filter(date = self.date_url).values_list('hour','minute').distinct().order_by('hour','minute')

        context['user'] = self.request.user
        context['days'] = [self.date_url]
        context['hours'] = hours

        return context


class SearchTalkListView(ListView):
    """ View utilizada para mostrar as palestras por dia"""

    template_name = "grade/search_talk_list.html"

    def get_queryset(self):
        self.query = self.request.GET.get('search', '')

    def get_context_data(self, **kwargs):
        context = super(SearchTalkListView, self).get_context_data(**kwargs)

        if self.query:
            qset = (
                Q(title__icontains=self.query) |
                Q(authors__name__icontains=self.query)
            )
            context['talks'] = Talk.objects.filter(qset).order_by('date', 'hour').distinct()
        else:
            context['talks'] = []

        context['user'] = self.request.user
        context['query'] = self.query

        return context


class AuthorDetailView(DetailView):
    """ View utilizada para mostrar o autor e sua lista de palestras """

    model = Author
    context_object_name = 'author'


class AboutView(TemplateView):
    """ View da página Sobre """

    template_name = "grade/about.html"


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
