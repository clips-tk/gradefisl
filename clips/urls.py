from django.conf.urls import patterns, url
from views import TalkListView, TalkDetailView, IndexView, AuthorDetailView, ZoneDetailView, RoomDetailView, NowListView, DayTalkListView, AboutView, SearchTalkListView
from django.views.generic import ListView
from clips.models import Zone, Room, Talk
from django.views.generic.base import RedirectView

urlpatterns = patterns('clips.views',
    url(r'^palestras/$', TalkListView.as_view(), name='talks'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^palestras/(?P<pk>\d+)/$', TalkDetailView.as_view(),
        name='talk'),
    url(r'^palestras/(?P<talk_id>\d+)/assistir/$', "choice_talk",
        name="choice_talk"),
    url(r"^gerar_clips/", 'gerar_clips', name="gerar_clips"),
    url(r'^palestrantes/(?P<pk>\d+)/$', AuthorDetailView.as_view(),
        name='author'),
    url(r'^trilhas/$', ListView.as_view(
        model=Zone,
        context_object_name="zone_list")),
    url(r'^trilhas/(?P<pk>\d+)/$', ZoneDetailView.as_view(),
    name='zone'),
    url(r'^salas/$', ListView.as_view(
        model=Room,
        context_object_name="rooms")),
    url(r'^salas/(?P<pk>\d+)/$', RoomDetailView.as_view(),
    name='room'),
    url(r'^dia/(\w+)/$', DayTalkListView.as_view()),
    url(r'^dia/$', ListView.as_view(
        queryset=Talk.objects.dates("date", "day"),
        template_name="clips/days_list.html",
        context_object_name="days")),
    url(r'^agora/$', NowListView.as_view(), name='now'),
    url(r'^sobre/$', AboutView.as_view(), name='about'),
    url(r'^busca/$', SearchTalkListView.as_view()),
    url(r'^code/$', RedirectView.as_view(
        url='https://github.com/clips-tk/clipsfisl'),
        name='code'),

)
