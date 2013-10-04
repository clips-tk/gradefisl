# coding: utf-8

from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, TemplateView, ListView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Q

# fisl
from clips.models import Room, Zone, Author, Talk


class IndexView(TemplateView):
    """ Homepage view """

    template_name = "clips/index.html"


class TalkDetailView(DetailView):
    """ View that shows Talk details """

    model = Talk
    context_object_name = 'talk'


class TalkListView(TemplateView):
    """ Show the Talks grouped by date and hour """

    template_name = "clips/talks_list.html"

    def get_context_data(self, **kwargs):
        context = super(TalkListView, self).get_context_data(**kwargs)

        days = Talk.objects.dates("date", "day")
        hours = ['8:50', '9:30', '10:10', '11:10', '11:50', '12:30', '14:00',
             '15:10', '15:50', '16:40', '17:20']

        context['user'] = self.request.user
        context['days'] = days
        context['hours'] = hours

        return context


class ZoneDetailView(DetailView):
    """ Show talks grouped by Zone """

    model = Zone
    template_name = "clips/zone_talk_list.html"

    def get_context_data(self, **kwargs):
        context = super(ZoneDetailView, self).get_context_data(**kwargs)

        days = self.get_object().talk_set.all().dates("date", "day")
        hours = ['8:50', '9:30', '10:10', '11:10', '11:50', '12:30', '14:00',
             '15:10', '15:50', '16:40', '17:20']

        context['zone'] = self.get_object()
        context['user'] = self.request.user
        context['days'] = days
        context['hours'] = hours

        return context


class RoomDetailView(DetailView):
    """ Show talks grouped by Room """

    model = Room
    template_name = "clips/room_talk_list.html"

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)

        days = self.get_object().talk_set.all().dates("date", "day")
        hours = ['8:50', '9:30', '10:10', '11:10', '11:50', '12:30', '14:00',
             '15:10', '15:50', '16:40', '17:20']

        context['zone'] = self.get_object()
        context['user'] = self.request.user
        context['days'] = days
        context['hours'] = hours

        return context


class NowListView(TemplateView):
    """ Show talks happening now and the talks of the next session """

    template_name = "clips/now_talk_list.html"

    def get_context_data(self, **kwargs):
        context = super(NowListView, self).get_context_data(**kwargs)

        context['user'] = self.request.user
        context['now'] = datetime.now()
        context['last_session'] = datetime.now() - timedelta(minutes=40)
        context['next_session'] = datetime.now() + timedelta(minutes=40)

        return context


class DayTalkListView(ListView):
    """ Show talks of the selected day """

    template_name = "clips/talks_list.html"

    def get_queryset(self):
        self.date_url = Talk.objects.dates("date", "day")[int(self.args[0])]

    def get_context_data(self, **kwargs):
        context = super(DayTalkListView, self).get_context_data(**kwargs)

        hours = ['8:50', '9:30', '10:10', '11:10', '11:50', '12:30', '14:00',
             '15:10', '15:50', '16:40', '17:20']

        context['user'] = self.request.user
        context['days'] = [self.date_url]
        context['hours'] = hours

        return context


class SearchTalkListView(ListView):
    """ Search Talks by title, abstract and authors name """

    template_name = "clips/search_talk_list.html"

    def get_queryset(self):
        self.query = self.request.GET.get('search', '')

    def get_context_data(self, **kwargs):
        context = super(SearchTalkListView, self).get_context_data(**kwargs)

        if self.query:
            qset = (
                Q(title__icontains=self.query) |
                Q(abstract__icontains=self.query) |
                Q(authors__name__icontains=self.query)
            )
            context['talks'] = Talk.objects.filter(qset).order_by('date').distinct()
        else:
            context['talks'] = []

        context['user'] = self.request.user
        context['query'] = self.query

        return context


class AuthorDetailView(DetailView):
    """ Show the details of an author """

    model = Author
    context_object_name = 'author'


class AboutView(TemplateView):
    """ View of the About page """

    template_name = "clips/about.html"


def clean_data():
    """ Clean the clips models """

    clips_models = [Room, Talk, Zone, Author]
    clear_data = lambda x: x.objects.all().delete()

    for clips_model in clips_models:
        clear_data(clips_model)


@login_required
def choice_talk(request, talk_id):
    talk = Talk.objects.get(id=talk_id)

    if not talk.listeners.filter(id=request.user.id).count():
        talk.listeners.add(request.user)
        talk.save()

    return HttpResponseRedirect(reverse('clips:talk', args=[talk_id]))


def gerar_rooms(json):
    for room in json['rooms']:
        if not Room.objects.filter(uid=room['room_id']).count():
            Room.objects.create(uid=room['room_id'],
                                capacity=room['capacity'],
                                name=room['name'],
                                translation=room['translation'],
                                position=room['position'])


def gerar_zones(json):
    for zone in json['zones']:
        if not Zone.objects.filter(uid=zone['zone_id']).count():
            Zone.objects.create(uid=zone['zone_id'], name=zone['name'])


def gerar_authors(json):
    for author in json['authors']:
#        if not Author.objects.filter(uid=author['author_id']).count():
        Author.objects.create(uid=author['author_id'],
                              candidate=author['candidate'],
                              name=author['name'])


def gerar_talks(json):
    gerar_rooms(json)
    gerar_zones(json)
    gerar_authors(json)

    for talk in json['talks']:
        if not Talk.objects.filter(area=talk['area_id']).count():
            t = Talk(room=Room.objects.get(uid=talk['room_id']),
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


def gerar_clips(request):
    data_json = open("public/json/data.json", "r").read()
    json = simplejson.loads(data_json)

    gerar_talks(json)

    return HttpResponse("clips gerada com sucesso!")
