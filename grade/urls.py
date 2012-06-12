from django.conf.urls.defaults import patterns, url
from views import TalkListView, TalkDetailView, IndexView, SearchView, AuthorDetailView
from django.views.generic import ListView
from grade.models import Zone

urlpatterns = patterns('grade.views',
    url(r'^palestras/$', TalkListView.as_view(), name='talks'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^busca/$', SearchView.as_view(), name='search'),
    url(r'^palestras/(?P<pk>\d+)/$', TalkDetailView.as_view(),
        name='talk'),
    url(r'^palestras/(?P<talk_id>\d+)/assistir/$', "choice_talk",
        name="choice_talk"),
    url(r"^gerar_grade/", 'gerar_grade', name="gerar_grade"),
    url(r'^palestrantes/(?P<pk>\d+)/$', AuthorDetailView.as_view(),
        name='author'),
    url(r'^trilhas/$', ListView.as_view(
        model=Zone,
        )),
)
